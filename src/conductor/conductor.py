import logging
import os
import signal
import sys
import threading
import time as timer
from datetime import datetime

import RPi.GPIO as GPIO
import vlc

from musician import *
from utils import *

# Pin assignments
MOTOR_VR_PIN = 12  # Motor speed
MOTOR_EL_PIN = 19  # Motor enable
SSR_PIN = 21  # Solid State Relay
AUX = 18  # AUX output
REED_SENSOR = 5


MOTOR = None
OPEN_HOUR = parse_time_from_string(get_env("OPEN_HOUR", "08:00:00"))
CLOSE_HOUR = parse_time_from_string(get_env("CLOSE_HOUR", "20:00:00"))
TRACKS_TO_PLAY = int(get_env("TRACKS_TO_PLAY", 2))
BREAK_TIME = int(get_env("BREAK_TIME", 300))
TRAINSPOTTING = bool(get_env("TIMEKEEPER", 1))
TRAINSPOTTING_LIMIT = int(get_env("TIMEKEEPER_LIMIT", 40))
TRAINSPOTTING_DISTANCE = int(get_env("TIMEKEEPER_DISTANCE", 3))
TRAINSPOTTER = None


ready_to_log = True
ready_for_next_run = True
has_running_show = False
train_speed = 100
train_break_time = 2
latest_trainspotting = None


def setup():
    """Program initialization"""
    global MOTOR

    print("Choo! Choo! The train is booting..")

    # Configure IO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup([MOTOR_VR_PIN, MOTOR_EL_PIN, SSR_PIN], GPIO.OUT)
    GPIO.output([MOTOR_EL_PIN, SSR_PIN], GPIO.LOW)
    MOTOR = GPIO.PWM(MOTOR_VR_PIN, 8000)
    MOTOR.start(0)  # Is equal to zero speed
    if TRAINSPOTTING:
        GPIO.setup(REED_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(
            REED_SENSOR,
            GPIO.RISING,
            callback=trainspotter_trainspotting,
            bouncetime=500,
        )

    print("Ready!")


def loop():
    """Continous business logic"""
    global ready_for_next_run, ready_to_log, has_running_show

    GPIO.output(SSR_PIN, shop_is_open() or has_running_show)

    if shop_is_open() is True and ready_for_next_run is True:
        ready_for_next_run = False
        threading.Thread(target=run_show_sequence).start()

    if ready_to_log is True:
        threading.Thread(target=logging).start()


def run_show_sequence():
    """Handler for the show sequence"""
    global ready_for_next_run, has_running_show
    has_running_show = True

    # Play upbeat track
    upbeat_track = get_upbeat_track()
    upbeat_track_path = os.path.join(get_vault_path(), upbeat_track)
    print(f"Now playing upbeat track {upbeat_track}")
    players = vlc.MediaPlayer(upbeat_track_path)
    players.audio_set_volume(40)
    players.play()
    timer.sleep(players.get_length() / 1000)

    # Start train motor
    GPIO.output(MOTOR_EL_PIN, GPIO.HIGH)
    MOTOR.ChangeDutyCycle(train_speed)

    # Play music playlist
    for track in get_sub_playlist(TRACKS_TO_PLAY):
        if not shop_is_open():
            break
        print(f"Now playing music track {track}")
        players.set_media(os.path.join(get_vault_path(), track))
        players.audio_set_volume(20)
        players.play()
        timer.sleep(players.get_length() / 1000)
        players.audio_set_volume(0)

        if TRAINSPOTTING:
            stop_time = datetime.now().time()
            stop_time_limit = stop_time + datetime.timedelta(
                seconds=TRAINSPOTTING_LIMIT
            )
            while stop_time > latest_trainspotting:
                timer.sleep(0.2)
                if datetime.now.time() > stop_time_limit:
                    send_alert("Train is late")
                    break

            timer.sleep(TRAINSPOTTING_DISTANCE)

    # Disable train motor
    step_size = 1
    for dc in range(train_speed, 0, -step_size):
        MOTOR.ChangeDutyCycle(dc)
        timer.sleep(train_break_time / train_speed * step_size)
    MOTOR.ChangeDutyCycle(0)
    GPIO.output(MOTOR_EL_PIN, GPIO.LOW)
    timer.sleep(1)

    # Pause until next
    has_running_show = False
    timer.sleep(BREAK_TIME)
    ready_for_next_run = True


def logging():
    """Log handler"""
    global ready_to_log, has_running_show, ready_for_next_run
    ready_to_log = False
    print(
        f"shop is {['closed', 'open'][shop_is_open()]}\tshow is running {has_running_show}\tready for next show {ready_for_next_run}"
    )
    timer.sleep(1)
    ready_to_log = True


def shop_is_open():
    """True if current clock is in the range [OPEN_HOUR, CLOSE_HOUR]"""
    global OPEN_HOUR, CLOSE_HOUR
    return OPEN_HOUR <= datetime.now().time() <= CLOSE_HOUR


def trainspotter_trainspotting(channel):
    global latest_trainspotting
    if latest_trainspotting is None:
        latest_trainspotting = datetime.now().time()
        print(f"Train was spotted for the first time at {latest_trainspotting}")
        return
    prior_trainspotting = latest_trainspotting
    latest_trainspotting = datetime.now().time()
    print(
        f"Train was spotted! It was {latest_trainspotting - prior_trainspotting} ago it last was spotted"
    )
    return


def send_alert(message):
    print(f"ALERT: {message}")


if __name__ == "__main__":
    killer = GracefulKiller()

    try:
        setup()
        while not killer.kill_now:
            loop()
    except KeyboardInterrupt as ex:
        print("Gracefully shutting down")
    finally:
        GPIO.cleanup()
        print("Shutting down")
        sys.exit(0)
