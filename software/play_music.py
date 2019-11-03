import os
import glob
import subprocess
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

sleep(1)

usb_dir = None
tracks = None

flag = None
play_index = None
st = None

RUN_MUSIC = True

def main():

    global flag, play_index, st
    flag = 1
    play_index = 0
    st = 0

    while RUN_MUSIC:
        if flag == 1:

            flag = 0
            player = subprocess.Popen(['omxplayer', '-o', 'local', tracks[play_index]], stdin=subprocess.PIPE)
            playing = player.poll()
            st = 0

            print(flag, st, playing, play_index)

            if (playing == 0 and st == 0):
                flag = 1
                play_index = (play_index + 1) % len(tracks)

        sleep(0.1)


def read_track_names():
    global usb_dir, tracks
    usb_dir = '/media/usb'
    tracks = glob.glob( os.path.join(usb_dir, '*.mp3'))

    print ('Tracks to be shuffled from:')
    print ('\n'.join(tracks))





if __name__ == "__main__":

    # kill any existing player instances
    subprocess.Popen(['killall', 'omxplayer.bin'], stdin=subprocess.PIPE)

    read_track_names()
    main()
