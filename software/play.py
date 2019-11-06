import serial, time, struct, os, glob, random
from pydub import AudioSegment, effects
from pydub.playback import play


# device paths
ARDUINO_PORT = '/dev/ttyUSB0'
MUSIC_USB_PATH = '/media/usb'

# serial readings
arduino = None
struct_form = 'HB?'
size = struct.calcsize(struct_form)

last_played_track = None
stop_music_time = None

playing_volume = -20


###########################
# CALLED ONCE BEFORE LOOP #
###########################
def setup():
  global  arduino, stop_music_time

  # PySerial setup
  arduino = serial.Serial(
    port=ARDUINO_PORT,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
  )

  stop_music_time = time.time()



##############################################
# REPEATS THROUGHOUT THE LIFE OF THE PROGRAM #
##############################################
def loop():

  global arduino, stop_music_time

  # read data from Arduino
  state = arduino.read(size)
  arduino.reset_input_buffer() #.flushInput()
  data = struct.unpack(struct_form, state)
  speed = data[1]
  is_motor_running = data[2]
  print('time: {}\tstop music: {}\treading: {}'.format(time.time()//1, stop_music_time//1, data), end='\r', flush=True)

  # start music
  if (speed > 0) and (is_motor_running == True) and (time.time() > stop_music_time):

    # get a track to play
    track_path = get_new_track()
    _track = AudioSegment.from_file(track_path, format='mp3')

    # adjust volume
    track = match_target_amplitude(_track, playing_volume)
    print('\nplaying: {}'.format(track_path))
    play(track)
    stop_music_time = time.time() + (track.duration_seconds/1000) + 5



########################################################
# RETURNS A NEW TRACK, THAT IS NOT THE PREVIOUS PLAYED #
########################################################
def get_new_track():
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



###############################
# FETCH TRACKS FROM USB STICK #
###############################
def get_playlist():
  return glob.glob( os.path.join(MUSIC_USB_PATH, '*.mp3'))



################################
# ADJUSTS AMPLITUDE FOR TRACKS #
################################
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)



#################
# PROGRAM ENTRY #
#################
def main():
  setup()
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
