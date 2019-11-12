import serial, time, datetime, struct, os, random, subprocess, math
from glob import glob
from pydub import AudioSegment, effects
from pydub.playback import play
import RPi.GPIO as GPIO
from mutagen.mp3 import MP3

# music variables
MUSIC_LIB_PATH = './../music'  # '/media/usb0'
last_played_track = None
stop_music_time = 0
playing_volume = -20
tracks_to_play = 1
player_start_delay = 15
player = None


# motor variables
motor_vr_pin = 12
motor_zf_pin = 16
motor_vr = None
motor_zf = None

# train graph
MAX_SPEED = 50
MIN_SPEED = 0
BOOT_COEF = 4
BREAK_COEF = 2
GRAPH_TRANSITION_THRESHOLD = MAX_SPEED / 2 # between 0.01 and (MAX_SPEED-0.01); (MAX_SPEED/2) will eliminate the feature

# managing variable
OPEN_HOUR = datetime.time(3, 0, 0)
CLOSE_HOUR = datetime.time(20, 0, 0)

current_time_unix = 0
current_time = 0
progress_time_offset = 0
run_interval = 30
stopped_interval = 30

run_train = False
run_music = False

playlist_duration = 0


def setup():
  """PROGRAM INITIALIZATION"""
  print('Choo! Choo! The train is booting..')

  global motor_vr, motor_vr_pin, motor_zf, motor_zf_pin

  # configure motor IO
  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False)
  GPIO.setup(motor_vr_pin, GPIO.OUT)
  GPIO.setup(motor_zf_pin, GPIO.OUT)
  GPIO.output(motor_zf_pin, GPIO.LOW)
  motor_vr = GPIO.PWM(motor_vr_pin, 50)
  motor_vr.start(0)

  print('Ready!')
  time.sleep(1)




def loop():
  """MAIN PROGRAM LOOP"""
  global motor_vr, motor_zf, current_time_unix, current_time, run_train, run_music, progress_time_offset, stop_music_time, MIN_SPEED, playlist_duration, run_interval


  # time trackers
  current_time_unix = time.time()
  current_date = datetime.datetime.now().time()
  
  progress = (current_time_unix+progress_time_offset) % (run_interval+stopped_interval)
  speed = MIN_SPEED

  # run constellation only within the shops opening hours
  if is_shop_open(current_date) is True:

    # begin music
    if (progress-player_start_delay) < (5-player_start_delay) and run_music == False:
      print('getting playlist')
      run_music = True
      track_paths = get_sub_playlist()
      tracks = [MP3(mp3_file) for mp3_file in track_paths]
      playlist_duration = sum(track.info.length for track in tracks)
      run_interval = playlist_duration
      stop_music_time = playlist_duration + current_time_unix


    # set train speed
   # _progress = (current_time_unix+progress_time_offset) % int(playlist_duration)
    speed = int(speed_graph(progress, playlist_duration+stopped_interval))

  if current_time_unix > stop_music_time and run_music == True:
    print('arming player')
    run_music = False


  # constrain speed
  speed = min(100, max(0, speed))
  motor_vr.ChangeDutyCycle(speed)
  print('open: {} {:.02f} + {:.02f} = {:.02f} {:.02f} {}'.format(is_shop_open(current_date), current_time_unix, playlist_duration, stop_music_time, progress, speed))




def speed_graph(progress, duration=run_interval):
  """COMPUTES A SPEED USING SIGMOID FUNCTIONS BASED ON THE GIVEN PROGRESS"""
  global MAX_SPEED, GRAPH_TRANSITION_THRESHOLD, BOOT_COEF, BREAK_COEF

  # shared computations
  numerator = math.log( (MAX_SPEED / GRAPH_TRANSITION_THRESHOLD) - 1)

  # boot graph
  boot_graph_offset = (numerator / math.log(BOOT_COEF))
  boot_vector = MAX_SPEED / (1 + BOOT_COEF**(-progress + boot_graph_offset))

  # break graph
  break_graph_offset = (numerator / math.log(BREAK_COEF)) - duration
  break_vector = MAX_SPEED / (1 + BREAK_COEF**(progress + break_graph_offset))

  return boot_vector + break_vector - MAX_SPEED




def is_shop_open(date):
    """Return true if x is in the range [OPEN_HOUR, CLOSE_HOUR]"""
    global OPEN_HOUR, CLOSE_HOUR
    if OPEN_HOUR <= CLOSE_HOUR:
        return OPEN_HOUR <= date <= CLOSE_HOUR
    else:
        return OPEN_HOUR <= date or date <= CLOSE_HOUR



def get_sub_playlist():
  """RETURNS A NEW SUBPLAYLIST FOR THIS RUN"""
  sublist = []
  for i in range(tracks_to_play):
    sublist.append(get_new_track())
  return sublist




def get_new_track():
  """RETURNS A NEW TRACK, THAT IS NOT THE PREVIOUS PLAYED"""
  global last_played_track

  # get playliste and pick track
  playlist = get_playlist()
  track = random.choice(playlist)

  # exclude last played track, if others are available
  if len(playlist) > 1 and last_played_track != None:
    while last_played_track == track:
      track = random.choice(playlist)

  last_played_track = track
  return track



def get_playlist():
  """FETCH TRACKS FROM USB STICK"""
  return glob(os.path.join(MUSIC_LIB_PATH, '*.mp3'))



def match_target_amplitude(sound, target_dBFS):
    """ADJUSTS AMPLITUDE FOR TRACKS"""
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)




def copy_convert_tracks():
  """COPIES SONGS TO TEMPORARY DIRECTORY AND ADJUSTS GAIN"""
  pass



def main():
  try:
    setup()
    while True:
      loop()
  except KeyboardInterrupt:
    pass

  motor_vr.stop()
  GPIO.cleanup()



if __name__ == '__main__':
  main()

