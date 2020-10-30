import os, random, time as timer
import RPi.GPIO as GPIO
import numpy as np

from datetime import datetime, time
from glob import glob
from mutagen.mp3 import MP3
from omxplayer.player import OMXPlayer


motor_vr_pin = 12
motor_relay_pin = 13
ssr_pin = 11


# music variables
MUSIC_LIB_DIR = '/music'
NORMALIZED_LIB_DIR = '.normalized_tracks'


last_played_track = None
player = None
playlist = []
run_music = False
new_playlist = True
playlist_duration = 0
track_stop_time = 0
tracks_to_play = 2


# motor and speed
motor = None
MAX_SPEED = 50
MIN_SPEED = 10
BOOT_COEF = 4
BREAK_COEF = 2
GRAPH_TRANSITION_THRESHOLD = 5 # between 0 and MAX_SPEED: (MAX_SPEED/2) will eliminate the feature


# managing variables
OPEN_HOUR = time(8, 0, 0)
CLOSE_HOUR = time(21, 45, 0)
progress_start_time = 0
default_run_time = 40
run_time = default_run_time
stop_time = (5 * 60)
progress = 0
print_time = 0
do_print = False


def setup():
  """program initialization"""
  global motor, motor_vr_pin, progress_start_time, MUSIC_LIB_DIR

  print('Choo! Choo! The train is booting..')

  # configure IO
  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False)
  GPIO.setup(motor_vr_pin, GPIO.OUT)
  GPIO.setup(ssr_pin, GPIO.OUT)
  GPIO.setup(motor_relay_pin, GPIO.OUT)

  GPIO.output(ssr_pin, GPIO.LOW)
  GPIO.output(motor_relay_pin, GPIO.LOW)

  motor = GPIO.PWM(motor_vr_pin, 1000)
  motor.start(100-0)

  if os.path.exists(os.path.join(MUSIC_LIB_DIR, NORMALIZED_LIB_DIR)):
    MUSIC_LIB_DIR = os.path.join(MUSIC_LIB_DIR, NORMALIZED_LIB_DIR)
    print('Found normalized tracks directory ->', MUSIC_LIB_DIR)

  current_date = datetime.now()
  current_time = datetime.timestamp(current_date)
  progress_start_time = current_time
  progress = 0

  print('found upbeat playlist:\n', get_upbeat_playlist(), '\nand playlist:\n', get_playlist(), '\n')
  print('Ready!')


def loop_async():
  """ main loop that implements a non-blocking strategy """
  global motor, progress_start_time, MIN_SPEED, run_time, stop_time, new_playlist, player, playlist, track_stop_time, tracks_to_play, default_run_time, print_time, progress, do_print

  # time trackers
  current_date = datetime.now()
  current_time = datetime.timestamp(current_date)
  shop_is_open = is_shop_open(current_date)
  progress = current_time - progress_start_time
  speed = MIN_SPEED

  if shop_is_open is True:

    # compute speed
    speed = 100 if progress < 2 else speed_graph(progress, duration=run_time)

    # populate playlist
    if new_playlist is True:
      new_playlist = False
      do_print = True
      playlist = []
      playlist_duration = default_run_time
      run_time = default_run_time

      # try to populate playlist
      try:
        playlist += [get_upbeat_track()]
      except:
        print('No upbeat tracks available')
      try:
        playlist += get_sub_playlist(tracks_to_play)
      except:
        print('No music tracks available')


      # estimate run duration for this interval
      if playlist:
        try:
          playlist_duration = sum(track.info.length for track in [MP3(mp3_file) for mp3_file in playlist])
          run_time = playlist_duration
          print('New run time for this interval')
        except:
          run_time = default_run_time
          print('Default run time for this interval')

  # if shop is not open
  else:
    progress_start_time = current_time
    speed = 0
    if playlist:
      print('Erasing remaing songs from playlist, due to closed shop')
      playlist = []


  # drain playlist for tracks
  if playlist:
    if current_time > track_stop_time:

      # create or reuse player instance
      try:
        player.load(playlist[0])
        print('Reusing player')
      except:
        player = OMXPlayer(playlist[0])
        print('New player')

      # next stop
      try:
        track_stop_time = player.duration() + current_time
      except:
        print('Current playing track duration exception')
        track_stop_time = default_run_time + current_time
        run_time = default_run_time

      playlist.pop(0)


  # reset and prepare for new run
  if progress > (run_time+stop_time) and new_playlist is False:
    progress_start_time = current_time
    new_playlist = True
    do_print = True

  # write IO
  relay_on = int(speed) > (MIN_SPEED + 0.5) and shop_is_open
  GPIO.output(motor_relay_pin, relay_on)
  GPIO.output(ssr_pin, shop_is_open)
  motor.ChangeDutyCycle(100-int(speed))


  # print stuff
  if current_time > print_time or do_print is True:
    print_time = current_time + 1
    do_print = False
    print('{}  (shop is {})   |   progress: {:03.0f}, {:03.0f}, {:03.0f} ({:03.0f}%)  speed: {:.02f}  (relay {})   |  stop music at: {:.02f}  playlist: {}'.format(current_date, ("open" if shop_is_open else "closed"), progress, run_time, stop_time, progress/(run_time+stop_time)*100, speed, "on" if relay_on else "off", track_stop_time, [track.split('/')[-1] for track in playlist]), end='\n',flush=False)



def speed_graph(progress, duration):
  """computes a speed graph from the given progress and duration times"""
  global MAX_SPEED, MIN_SPEED, GRAPH_TRANSITION_THRESHOLD, BOOT_COEF, BREAK_COEF

  SPEED = MAX_SPEED - MIN_SPEED

  # lower bounds (pick largest number)
  progress = max(0, progress)
  duration = max(30, duration)

  # shared computations
  numerator = np.log((SPEED / GRAPH_TRANSITION_THRESHOLD) - 1)

  # boot graph
  boot_graph_offset = (numerator / np.log(BOOT_COEF))
  boot_vector = SPEED / (1 + BOOT_COEF**(-progress + boot_graph_offset))

  # break graph
  break_graph_offset = (numerator / np.log(BREAK_COEF)) - duration
  break_vector = SPEED / (1 + BREAK_COEF**(progress + break_graph_offset))

  # compute final speed vector
  speed_vector = boot_vector + break_vector - SPEED + MIN_SPEED

  # constrain and return
  return min(100, max(0, speed_vector))




def is_shop_open(date):
    """return true if x is in the range [OPEN_HOUR, CLOSE_HOUR]"""
    global OPEN_HOUR, CLOSE_HOUR
    if OPEN_HOUR <= CLOSE_HOUR:
        return OPEN_HOUR <= date.time() <= CLOSE_HOUR
    else:
        return OPEN_HOUR <= date.time() or date.time() <= CLOSE_HOUR



def get_sub_playlist(tracks_to_play):
  """returns a playlist fraction"""
  #return random.sample(get_playlist(), k=tracks_to_play)

  sublist = []
  for i in range(tracks_to_play):
    sublist.append(get_new_track())
  return sublist


def get_upbeat_playlist():
  """ returns a list containing all upbeat tracks """
  playlist = get_full_playlist()
  upbeat_tracks = [track for track in playlist if 'upbeat' in track]
  return upbeat_tracks


def get_upbeat_track():
  """returns path to a random upbeat track"""
  try:
    upbeat_tracks = get_upbeat_playlist()
    return random.choice(upbeat_tracks)
  except:
    return []


def get_new_track():
  """returns a new track, that was not the previous"""
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
  """gets the full playlist without the intro track"""
  return np.setdiff1d(get_full_playlist(), get_upbeat_playlist())



def get_full_playlist():
  """gets all tracks from the usb"""
  return glob(os.path.join(MUSIC_LIB_DIR, '*.mp3'))


def main():
  global player, motor

  try:
    setup()
    while True:
      loop_async()
  except KeyboardInterrupt:
    pass

  try:
    motor.stop()
    GPIO.cleanup()
  except:
    print('IO termination exception')

  try:
    player.stop()
  except:
    print('Player termination exception')


if __name__ == '__main__':
  main()