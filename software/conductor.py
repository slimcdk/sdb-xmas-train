import serial, time, datetime, struct, os, random, subprocess, math
from glob import glob
from pydub import AudioSegment, effects
from pydub.playback import play
import RPi.GPIO as GPIO


# music variables
MUSIC_LIB_PATH = './../music'  # '/media/usb0'
last_played_track = None
stop_music_time = None
playing_volume = -20
tracks_to_play = 2
tracks_played = 0
player = None


# motor variables
motor_vr_pin = 12
motor_zf_pin = 14
motor_vr = None
motor_zf = None

# train graph
MAX_SPEED = 50
MIN_SPEED = 0
BOOT_COEF = 4
BREAK_COEF = 2
GRAPH_TRANSITION_THRESHOLD = 0.1

# managing variable
OPEN_HOUR = datetime.time(8, 0, 0)
CLOSE_HOUR = datetime.time(20, 0, 0)

current_time_unix = None
current_time = None
progress_time_offset = None
run_interval = 50

run_train = False
run_music = False




def setup():
  global motor_vr, motor_vr_pin, motor_zf, motor_zf_pin, current_time_unix, progress_time_offset, run_interval, stop_music_time

  print('Choo! Choo! The train is booting..')

  # configure motor IO
  GPIO.setmode(GPIO.BOARD)
  # GPIO.setwarnings(False)
  GPIO.setup(motor_vr_pin, GPIO.OUT)
#  GPIO.setup(motor_zf_pin, GPIO.OUT)
#  GPIO.output(motor_zf_pin, GPIO.LOW)
  motor_vr = GPIO.PWM(motor_vr_pin, 1000)  # channel=12 frequency=50Hz
  motor_vr.start(0)

  current_time_unix = int(time.time())
  progress_time_offset = 0 - int(current_time_unix % run_interval)
  stop_music_time = current_time_unix

  subprocess.Popen(['killall', 'omxplayer.bin'], stdin=subprocess.PIPE)
  if player != None:
    player.stdin.write('q')
    player.kill()

  print('Ready!')
  time.sleep(1)


def loop():
  global motor_vr, motor_zf, current_time_unix, current_time, run_train, run_music, tracks_played, progress_time_offset, stop_music_time

  # time trackers
  current_time_unix = time.time()
  current_time = datetime.datetime.now().time()
  progress = (current_time_unix+progress_time_offset) % run_interval
  #print(current_time_unix, progress, stop_music_time)


  # run constellation only within the stores opening hours
  if time_within_openhours(current_time) is True:

    # begin music
    if progress < 3 and run_music == False:
      run_music = True
      track_paths = get_sub_playlist()
      tracks = [AudioSegment.from_mp3(mp3_file) for mp3_file in track_paths]
      stop_music_time = int(sum(track.duration_seconds for track in tracks)) + current_time_unix

  if current_time_unix > stop_music_time:
    run_music = False



  time.sleep(1)

  #set output
  speed = speedgraph(progress)
  print('{:.02f} {:.02f}'.format(progress, speed))
  #motor.changeDutyCycle(speed)




def speedgraph(progress):
  """COMPUTES A SPEED BASED ON THE GIVEN PROGRESS"""
  global MAX_SPEED, GRAPH_TRANSISTION_THRESHOLD, BOOT_COEF, BREAK_COEF, run_interval

  # find transition points (progress timestamps) for speed changes
  numerator = math.log( (MAX_SPEED / (MAX_SPEED-GRAPH_TRANSITION_THRESHOLD)) - 1)
  boot_stop_time = (numerator / -math.log(BOOT_COEF)) * 2
  break_start_time = (numerator / math.log(BREAK_COEF)) * 2 + run_interval

  print(boot_stop_time, break_start_time)

  # determine which graph should be used to compute speed
  speed = MIN_SPEED
  if progress < boot_stop_time:
    """BOOTING"""
    speed = bootgraph(progress)

  elif boot_stop_time < progress < break_start_time:
    """NORMAL"""
    speed = MAX_SPEED

  else:
    """BREAKING"""
    speed = breakgraph(progress)

  return speed



def bootgraph(progress):
  """COMPUTES THE ACCELERATION FOR THE TRAIN USING SIGMOID FUNCTION"""

  global MAX_SPEED, BOOT_COEF, run_interval, GRAPH_TRANSITION_THRESHOLD
  timeoffset = math.log((MAX_SPEED/GRAPH_TRANSITION_THRESHOLD) - 1) / math.log(BOOT_COEF)
  return MAX_SPEED / (1 + BOOT_COEF**(-progress+timeoffset))


def breakgraph(progress):
  """COMPUTES THE DECELERATION FOR THE TRAIN USING SIGMOID FUNCTION"""

  global MAX_SPEED, BREAK_COEF, run_interval, GRAPH_TRANSITION_THRESHOLD
  timeoffset = (math.log((MAX_SPEED/GRAPH_TRANSITION_THRESHOLD) - 1) / math.log(BREAK_COEF)) - run_interval
  return MAX_SPEED / (1 + BREAK_COEF**(progress+timeoffset))




def time_within_openhours(x):
    """Return true if x is in the range [OPEN_HOUR, CLOSE_HOUR]"""
    global OPEN_HOUR, CLOSE_HOUR

    if OPEN_HOUR <= CLOSE_HOUR:
        return OPEN_HOUR <= x <= CLOSE_HOUR
    else:
        return OPEN_HOUR <= x or x <= CLOSE_HOUR



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
#  motor_zf.stop()
  GPIO.cleanup()



if __name__ == '__main__':
  main()

