import os, random, time as timer
import RPi.GPIO as GPIO
import numpy as np

from datetime import datetime, time
from glob import glob
from mutagen.mp3 import MP3
from omxplayer.player import OMXPlayer




def setup():
  """program initialization"""

  print('Choo! Choo! The train is booting..')
  print('Ready!')


def loop():
  """ main loop that implements a non-blocking strategy """
  
  # time trackers
  current_date = datetime.now()
  current_time = datetime.timestamp(current_date)
  print(current_time)
  timer.sleep(3)


def main():
  try:
    setup()
    while True:
      loop()
  except KeyboardInterrupt:
    pass


if __name__ == '__main__':
  main()
