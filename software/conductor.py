import os, random, math, time as tm
from datetime import datetime, timedelta, time
from glob import glob
import RPi.GPIO as GPIO
from mutagen.mp3 import MP3
from omxplayer.player import OMXPlayer
import numpy as np

"""CONSTANTS"""
# GPIO
motor_vr_pin = 12
ssr_pin =      11


# music variables
MUSIC_LIB_PATH = 'music'
last_played_track = None
stop_music_time = 0
player = None
playlist = []
run_music = False
start_music = True
playlist_duration = 0
new_player = True
track_stop_time = 0
tracks_to_play = 1


# motor variables
motor = None


# train speed graph
MAX_SPEED = 50
MIN_SPEED = 0
BOOT_COEF = 4
BREAK_COEF = 2
GRAPH_TRANSITION_THRESHOLD = 5 # between 0 and MAX_SPEED: (MAX_SPEED/2) will eliminate the feature

# managing variable
OPEN_HOUR = time(18, 15, 0)
CLOSE_HOUR = time(20, 0, 0)
boot_time_offset = 0

run_time = 30
stop_time = (10 * 60)

def setup():
  """program initialization"""
  print('Choo! Choo! The train is booting..')

  global motor, motor_vr_pin, boot_time_offset

  # configure motor IO
  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False)
  GPIO.setup(motor_vr_pin, GPIO.OUT)
  GPIO.setup(ssr_pin, GPIO.OUT)

  GPIO.output(ssr_pin, GPIO.LOW)

  motor = GPIO.PWM(motor_vr_pin, 50)
  motor.start(0)

  boot_time_offset = datetime.timestamp(datetime.now())
  print('found upbeat playlist:\n', get_upbeat_playlist(), '\nand playlist:\n', get_playlist(), '\n')
  print('Ready!')
  print('date\t\t\t\topen\tprogress\t(run time, stop time)\t\tspeed\ttracks\tnew music\tnew player\tends at')
  tm.sleep(1)


def loop_async():
  """main loop that implements a non-blocking strategy"""
  global motor, boot_time_offset, MIN_SPEED, run_time, stop_time, start_music, player, playlist, track_stop_time, new_player, tracks_to_play

  # time trackers
  current_date = datetime.now()
  shop_is_open = is_shop_open(current_date)
  current_time = datetime.timestamp(current_date)
  progress = current_time - boot_time_offset
  speed = MIN_SPEED

  if shop_is_open is True:

    # populate playlist
    if start_music is True:
      start_music = False
      try:
        playlist = [get_upbeat_track()] + get_sub_playlist(tracks_to_play)
        playlist_duration = sum(track.info.length for track in [MP3(mp3_file) for mp3_file in playlist])
        print('playlist', playlist, 'has length', playlist_duration)
        run_time = playlist_duration
        new_player = True
      except:
        print('Could not get playlist!')
        playlist = []

      print('date\t\t\t\topen\tprogress\t(run time, stop time)\t\tspeed\ttracks\tnew music\tnew player\tends at')

    # compute speed
    speed = speed_graph(progress, duration=run_time)


  # if playlist has tracks
  if playlist:
    if current_time > track_stop_time:
      if new_player is True:
        new_player = False
        player = OMXPlayer(playlist[0])
        playlist.pop(0)
      else:
        player.load(playlist[0])
        playlist.pop(0)
      track_stop_time = player.duration() + current_time # + 1000


  # reset and prepare for new run
  if progress > run_time+stop_time and start_music is False:
    boot_time_offset = current_time
    start_music = True


  motor.ChangeDutyCycle(int(speed))
  GPIO.output(ssr_pin, shop_is_open)



  print('{}\t{}\t{:06.02f} ({:03.0f}%)\t({:.02f}, {:.02f})\t\t{:.02f}\t{}\t{}\t\t{}\t\t{:.02f}'.format(current_date, shop_is_open, progress, progress/(run_time+stop_time)*100, run_time, stop_time, speed, len(playlist), start_music, new_player, track_stop_time), end='\r',flush=False)




def loop_blocking():
  """main loop that utilizes sleep functions"""
  global motor, stop_time, MIN_SPEED

  if is_shop_open(datetime.now()):

    playlist = get_sub_playlist(1)
    print(playlist)

    player = OMXPlayer(get_upbeat_track())
    tm.sleep(player.duration())
    motor.ChangeDutyCycle(50)

    for track in playlist:
      player.load(track, False)
      print('playing track', player.get_filename(), 'with duration', player.duration())
      time.sleep(player.duration())
    player.stop()

    motor.ChangeDutyCycle(0)
    tm.sleep(stop_time)

  else:
    motor.ChangeDutyCycle(0)



def speed_graph(progress, duration):
  """computes a speed graph from the given progress and duration times"""
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
  playlist = get_full_playlist()
  upbeat_tracks = [track for track in playlist if 'upbeat' in track]
  return upbeat_tracks


def get_upbeat_track():
  """returns path to a random upbeat track"""
  upbeat_tracks = get_upbeat_playlist()
  if not upbeat_tracks:
    return None
  return random.choice(upbeat_tracks)


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
  return glob(os.path.join(MUSIC_LIB_PATH, '*.mp3'))



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

