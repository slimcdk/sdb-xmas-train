import os, threading, logging, sys, signal, time as timer, RPi.GPIO as GPIO
from datetime import datetime
from omxplayer.player import OMXPlayer

from musician import *
from utils import *

# Pin assignments
GPIO11        = 11  # Solid State Relay
GPIO19        = 19  # AUX output
MOTOR_VR_PIN  = 12  # Motor speed
MOTOR_EL_PIN  = 13  # Motor enable

MOTOR = None
OPEN_HOUR = parse_time_from_string(get_env('OPEN_HOUR', '08:00:00'))
CLOSE_HOUR = parse_time_from_string(get_env('CLOSE_HOUR', '20:00:00'))
TRACKS_TO_PLAY = int(get_env('TRACKS_TO_PLAY', 2))
BREAK_TIME = int(get_env('BREAK_TIME', 300))

ready_to_log = True
ready_for_next_run = True
has_running_show = False


def setup():
  """Program initialization"""
  global MOTOR

  print('Choo! Choo! The train is booting..')

  # Configure IO
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup([MOTOR_VR_PIN, MOTOR_EL_PIN, GPIO11], GPIO.OUT)

  GPIO.output([MOTOR_EL_PIN, GPIO11], GPIO.LOW)
  MOTOR = GPIO.PWM(MOTOR_VR_PIN, 1000)
  MOTOR.start(0) # Is equal to zero speed
  print('Ready!')



def loop():
  """Continous business logic"""
  global ready_for_next_run, ready_to_log, has_running_show
 
  GPIO.output(GPIO11, shop_is_open() or has_running_show)

  if shop_is_open() is True and ready_for_next_run is True:
      ready_for_next_run = False
      threading.Thread(target=run_show_sequence).start()

  if ready_to_log is True:
    threading.Thread(target=logging).start()



def run_show_sequence():
  """Handler for the show sequence"""
  global ready_for_next_run, has_running_show
  has_running_show = True

  # Enable train motor
  GPIO.output(MOTOR_EL_PIN, GPIO.HIGH)

  # Play upbeat track
  player = OMXPlayer(os.path.join(get_vault_path(), get_upbeat_track()))
  timer.sleep(player.duration())

  MOTOR.ChangeDutyCycle(100)
  timer.sleep(2)
  MOTOR.ChangeDutyCycle(50)

  # Play music playlist
  for track in get_sub_playlist(TRACKS_TO_PLAY):
    if not shop_is_open():
      break
    print(f'Now playing {track}')
    player.load(os.path.join(get_vault_path(), track))
    timer.sleep(player.duration())
  
  # Disable train motor
  MOTOR.ChangeDutyCycle(0)
  GPIO.output(MOTOR_EL_PIN, GPIO.LOW)

  # Pause until next
  has_running_show = False
  timer.sleep(BREAK_TIME)
  ready_for_next_run = True



def logging():
  """Log handler"""
  global ready_to_log, has_running_show, ready_for_next_run
  ready_to_log = False
  print (f"shop is {['closed', 'open'][shop_is_open()]}\tshow is running {has_running_show}\tready for next show {ready_for_next_run}")
  timer.sleep(1)
  ready_to_log = True



def shop_is_open():
    """True if current clock is in the range [OPEN_HOUR, CLOSE_HOUR]"""
    global OPEN_HOUR, CLOSE_HOUR
    return OPEN_HOUR <= datetime.now().time() <= CLOSE_HOUR



if __name__ == '__main__':
  killer = GracefulKiller()

  try:
    setup()
    while not killer.kill_now:
      loop()
  except KeyboardInterrupt as ex:
    print('Gracefully shutting down')
  finally:
    GPIO.cleanup()
    print("Shutting down")
    sys.exit(0)