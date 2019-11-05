import serial
import time
import struct
#import ctypes
import os
import glob
import subprocess
import RPi.GPIO as GPIO
import random
from mutagen.mp3 import MP3

# device paths
ARDUINO_PORT = '/dev/ttyUSB1'
MUSIC_USB_PATH = '/media/usb'

# serial reading
arduino = None
struct_form = 'HB?'
size = struct.calcsize(struct_form)

player = None
last_played_track = None
stop_music_time = None
music_is_playing = None


###########################
# Called once before loop #
###########################
def setup():
  global  arduino, player, stop_music_time, music_is_playing

  # PySerial setup
  arduino = serial.Serial(
    port=ARDUINO_PORT,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
  )

  # kill any existing player instances
  subprocess.Popen(['killall', 'omxplayer.bin'], stdin=subprocess.PIPE)
  if player != None:
    player.stdin.write('q')
    player.kill()

  #print('Playable tracks', getTrackPaths())
  stop_music_time = time.time()
  music_is_playing = False



##############################################
# Repeats throughout the life of the program #
##############################################
def loop():

  global arduino, player, stop_music_time, music_is_playing

  # read data from Arduino
  state = arduino.read(size)
  arduino.reset_input_buffer() #.flushInput()
  data = struct.unpack(struct_form, state)
  progress = data[0]
  speed = data[1]
  is_motor_running = data[2]

  print(data, end='\r', flush=True)

  # start player
  should_play = (speed > 0) # or is_motor_running == True)
  if should_play == True and music_is_playing == False:
    music_is_playing = True

    # get a track to play
    current_track_path = get_random_track()
    current_track = MP3(current_track_path)
    print('Track: {} has length {:.2f} seconds'.format(current_track_path, current_track.info.length))

    #settings for the current track
    vol = -20 - current_track.info.track_gain
    print('gain: {} \t peak: {} \t vol: {}'.format(current_track.info.track_gain, current_track.info.track_peak, vol))

    # start player and set time for player to terminate
    player = subprocess.Popen(['omxplayer', '-o', 'local', '--vol', '-{}'.format(vol), current_track_path], stdin=subprocess.PIPE)
    stop_music_time = time.time() + current_track.info.length + 1


  # terminate player
  if (time.time() > stop_music_time) and music_is_playing == True:
    music_is_playing = False
    print('Time to halt music -> ', end=' ')

    if player.poll() == True:
      print('force quitting player')
      player.kill()
    else:
      print('player already terminated')







#################################################################
# Returns a new (last played is excluded) random selected track #
#################################################################
def get_random_track():
  global last_played_track

  # fetch tracks from USB stick
  tracks = glob.glob( os.path.join(MUSIC_USB_PATH, '*.mp3'))

  # exclude last played track, if others are available
  if len(tracks) > 1 and last_played_track != None:
    tracks.remove(last_played_track)

  # return random selected track
  new_track = random.choice(tracks)
  last_played_track = new_track
  return new_track




##################################
# Normalizes gain for all tracks #
##################################
def convert_tracks():
  pass



#################
# Program entry #
#################
def main():
  setup()
  #time.sleep(2)


  try:
    while True:
      loop()
  except Exception as e:
    print('Wooops!', e)
    arduino.close()
    if player != None:
      player.kill()


if __name__ == '__main__':
  main()
