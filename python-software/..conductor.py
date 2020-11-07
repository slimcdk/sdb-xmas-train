
#!/usr/bin/python3

import os, random, threading, logging, time as timer
import RPi.GPIO as GPIO
import numpy as np
from datetime import datetime, time
from glob import glob
from mutagen.mp3 import MP3
from omxplayer.player import OMXPlayer

from music_vault import *
from utils import *

#logging.basicConfig(format='%(levelname)s-%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG,filename='/App/gpio.log')


pins = [13]

print(f"Setting up GPIO pins {pins}")
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(pins, GPIO.OUT)

print("Starting test loop")

for _ in range(30):
  GPIO.output(pins, 1)
  logging.info("Turning On")
  timer.sleep(1)

  GPIO.output(pins, 0)
  logging.info("Turning Off")
  timer.sleep(1)


track = get_new_track()
logging.info(f"Playing track {track}")
player = OMXPlayer(track)
timer.sleep(player.duration())

GPIO.cleanup()
exit(0)