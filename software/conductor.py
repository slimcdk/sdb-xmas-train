import time, datetime, os, random, subprocess, math
from glob import glob
from pydub import AudioSegment, effects
from pydub.playback import play
import RPi.GPIO as GPIO
from mutagen.mp3 import MP3
from omxplayer.player import OMXPlayer


# music variables
MUSIC_LIB_PATH = '/media/usb'
last_played_track = None
stop_music_time = 0
playing_volume = -20
player_start_delay = 15
player = None
playlist = []

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
GRAPH_TRANSITION_THRESHOLD = 5 # between 0 and MAX_SPEED: (MAX_SPEED/2) will eliminate the feature

# managing variable
OPEN_HOUR = datetime.time(3, 0, 0)
CLOSE_HOUR = datetime.time(20, 0, 0)


boot_time_offset = 0
run_interval = 40
stopped_interval = 30

run_train = False
run_music = False
start_music = True
playlist_duration = 0
new_player = True
track_stop_time = 0


def setup():
  """PROGRAM INITIALIZATION"""
  print('Choo! Choo! The train is booting..')

  global motor_vr, motor_vr_pin, motor_zf, motor_zf_pin, boot_time_offset, run_interval, stopped_interval, player

  # configure motor IO
  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False)
  GPIO.setup(motor_vr_pin, GPIO.OUT)
  GPIO.setup(motor_zf_pin, GPIO.OUT)
  GPIO.output(motor_zf_pin, GPIO.LOW)
  motor_vr = GPIO.PWM(motor_vr_pin, 50)
  motor_vr.start(0)

  boot_time_offset = time.time()

  print('Ready!')
  print('time\t\tprogress\t(run time, stop time)\tspeed\ttracks\tnew music\tnew player\tends at')
  # time.sleep(5)


def loop_async():
  """MAIN PROGRAM LOOP"""
  global motor_vr, motor_zf, run_train, run_music, boot_time_offset, stop_music_time, MIN_SPEED, playlist_duration, run_interval, stopped_interval, start_music, player, playlist, track_stop_time, new_player
  song = '\t\t\t'

  # time trackers
  current_time_unix = time.time()
  current_date = datetime.datetime.now().time()
  progress = current_time_unix - boot_time_offset
  speed = MIN_SPEED

  if is_shop_open(current_date) is True:

    # populate playlist
    if start_music is True:
      start_music = False
      try :
        playlist = [get_intro_track()] + get_sub_playlist(1)
        playlist_duration = sum(track.info.length for track in [MP3(mp3_file) for mp3_file in playlist])
        run_interval = playlist_duration
        new_player = True

      except:
        playlist = []

    # compute speed
    speed = speed_graph(progress, duration=run_interval)


  # if playlist has tracks
  if playlist:
    if current_time_unix > track_stop_time:
      if new_player is True:
        new_player = False
        player = OMXPlayer(playlist[0])
        playlist.pop(0)
      else:
        player.load(playlist[0])
        playlist.pop(0)
      track_stop_time = player.duration() + current_time_unix # + 1000


  # reset and prepare for new run
  if progress > run_interval+stopped_interval and start_music is False:
    boot_time_offset = current_time_unix
    start_music = True

  motor_vr.ChangeDutyCycle(int(speed))

  print('{:.02f}\t{:06.02f} ({:03.0f}%)\t({:.02f}, {:.02f})\t\t{:.02f}\t{}\t{}\t\t{}\t\t{:.02f}'.format(current_time_unix, progress, progress/(run_interval+stopped_interval)*100, run_interval, stopped_interval, speed, len(playlist), start_music, new_player, track_stop_time), end='\r',flush=False)




def loop_blocking():
  global motor_vr

  if is_shop_open(datetime.datetime.now().time()):

    playlist = get_sub_playlist(1)
    print(playlist)

    player = OMXPlayer(get_intro_track())
    time.sleep(player.duration())
    motor_vr.ChangeDutyCycle(50)

    for track in playlist:
      player.load(track, False)
      print('playing track', player.get_filename(), 'with duration', player.duration())
      time.sleep(player.duration())
    player.stop()

    motor_vr.ChangeDutyCycle(0)
    time.sleep(stopped_interval)

  else:
    motor_vr.ChangeDutyCycle(0)



def speed_graph(progress, duration):
  """COMPUTES A SPEED USING SIGMOID FUNCTIONS BASED ON THE GIVEN PROGRESS"""
  global MAX_SPEED, GRAPH_TRANSITION_THRESHOLD, BOOT_COEF, BREAK_COEF

  # lower bounds (pick largest number)
  progress = max(0, progress)
  duration = max(30, duration)

  # shared computations
  numerator = math.log( (MAX_SPEED / GRAPH_TRANSITION_THRESHOLD) - 1)

  # boot graph
  boot_graph_offset = (numerator / math.log(BOOT_COEF))
  boot_vector = MAX_SPEED / (1 + BOOT_COEF**(-progress + boot_graph_offset))

  # break graph
  break_graph_offset = (numerator / math.log(BREAK_COEF)) - duration
  break_vector = MAX_SPEED / (1 + BREAK_COEF**(progress + break_graph_offset))

  # compute final speed vector
  speed_vector = boot_vector + break_vector - MAX_SPEED

  # constrain and return
  return min(100, max(0, speed_vector))




def is_shop_open(date):
    """Return true if x is in the range [OPEN_HOUR, CLOSE_HOUR]"""
    global OPEN_HOUR, CLOSE_HOUR
    if OPEN_HOUR <= CLOSE_HOUR:
        return OPEN_HOUR <= date <= CLOSE_HOUR
    else:
        return OPEN_HOUR <= date or date <= CLOSE_HOUR



def get_sub_playlist(tracks_to_play):
  """RETURNS A NEW SUBPLAYLIST FOR THIS RUN"""
  #return random.sample(get_playlist(), k=tracks_to_play)

  sublist = []
  for i in range(tracks_to_play):
    sublist.append(get_new_track())
  return sublist



def get_intro_track():
  """RETURNS PATH TO THE INTRO TRACK"""
  playlist = get_full_playlist()
  if any('intro.mp3' in s for s in playlist):
    return os.path.join(MUSIC_LIB_PATH, 'intro.mp3')
  return None



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
  playlist = get_full_playlist()
  if get_intro_track() in playlist:
    playlist.remove(get_intro_track())
  return playlist


def get_full_playlist():
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
  global player, motor_vr

  try:
    setup()
    while True:
      loop_async()
  except KeyboardInterrupt:
    pass

  motor_vr.stop()
  GPIO.cleanup()
  player.quit()


if __name__ == '__main__':
  main()

