import os, time as timer
from glob import glob

from omxplayer.player import OMXPlayer


MUSIC_LIB_DIR = '/music'


def setup():
  """program initialization"""
  print('Choo! Choo! The train is booting..')
  print('Ready!')
  print(get_full_playlist())
  



def loop():
  """ main loop that implements a non-blocking strategy """
  print(get_full_playlist())
  timer.sleep(5)
  

def get_full_playlist():
  """gets all tracks from the usb"""
  global MUSIC_LIB_DIR
  return glob(os.path.join(MUSIC_LIB_DIR, '*.mp3'))



if __name__ == '__main__':
  setup()
  while True:
    loop()