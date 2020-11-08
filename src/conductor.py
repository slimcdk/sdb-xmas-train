import os, random, threading, logging, time as timer
import RPi.GPIO as GPIO
import numpy as np
from datetime import datetime
from omxplayer.player import OMXPlayer

from musician import *
from utils import *


SSR_PIN = 11
MOTOR_VR_PIN = 12
MOTOR_RELAY_PIN = 13

MOTOR = None

OPEN_HOUR = parse_time_from_string(get_env('OPEN_HOUR', '08:00:00'))
CLOSE_HOUR = parse_time_from_string(get_env('CLOSE_HOUR', '20:00:00'))


tracks_to_play = 2
stop_time = (5 * 60)
ready_to_log = True
ready_for_next_run = True



def setup():
  """program initialization"""
  global MOTOR

  print('Choo! Choo! The train is booting..')

  # Configure IO
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup([MOTOR_VR_PIN, MOTOR_RELAY_PIN, SSR_PIN], GPIO.OUT)

  GPIO.output([MOTOR_RELAY_PIN, SSR_PIN], GPIO.LOW)
  MOTOR = GPIO.PWM(MOTOR_VR_PIN, 1000)
  MOTOR.start(100-0)

  print('Ready!')



def loop():
  global ready_for_next_run, ready_to_log

  GPIO.output(SSR_PIN, shop_is_open())
 
  if shop_is_open() is True and ready_for_next_run is True:
      ready_for_next_run = False
      threading.Thread(target=run_show_sequence).start()

  if ready_to_log is True:
    ready_to_log = False
    threading.Thread(target=logging).start()



def run_show_sequence():
  global ready_for_next_run

  # Enable train motor
  GPIO.output(MOTOR_RELAY_PIN, GPIO.HIGH)

  # Play upbeat track
  player = OMXPlayer(os.path.join(get_vault_path(), get_upbeat_track()))

  MOTOR.ChangeDutyCycle(0) # equal to full speed
  timer.sleep(2)
  MOTOR.ChangeDutyCycle(50) # equal to half speed

  # Play music playlist
  for track in get_sub_playlist(2):
    if not shop_is_open():
      break
    print(f'Now playing {track}')
    player.load(os.path.join(get_vault_path(), track))
    timer.sleep(player.duration())
  
  # Disable train motor
  MOTOR.ChangeDutyCycle(100) # equal to zero speed
  GPIO.output(MOTOR_RELAY_PIN, GPIO.LOW)

  # Pause until next
  timer.sleep(stop_time)
  ready_for_next_run = True



def logging():
  global ready_to_log

  print (f"shop is {['closed', 'open'][shop_is_open()]}")

  timer.sleep(10)
  ready_to_log = True



def shop_is_open():
    """return true if current clock is in the range [OPEN_HOUR, CLOSE_HOUR]"""
    global OPEN_HOUR, CLOSE_HOUR
    return OPEN_HOUR <= datetime.now().time() <= CLOSE_HOUR



def main():
  setup()
  while True:
    loop()
  print("EXITING")
  
  GPIO.cleanup()

if __name__ == '__main__':
  main()