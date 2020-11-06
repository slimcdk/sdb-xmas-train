import os, random
import numpy as np

from datetime import datetime, time
from glob import glob
from mutagen.mp3 import MP3



# music variables
MUSIC_LIB_DIR = '/music'
NORMALIZED_LIB_DIR = '.normalized_tracks'

last_played_track = None



def get_sub_playlist(tracks_to_play):
  """returns a playlist fraction"""
  #return random.sample(get_playlist(), k=tracks_to_play)

  sublist = []
  for i in range(tracks_to_play):
    sublist.append(get_new_track())
  return sublist


def get_upbeat_playlist():
  """ returns a list containing all upbeat tracks """
  playlist = get_full_playlist()
  upbeat_tracks = [track for track in playlist if 'upbeat' in track]
  return upbeat_tracks


def get_upbeat_track():
  """returns path to a random upbeat track"""
  try:
    upbeat_tracks = get_upbeat_playlist()
    return random.choice(upbeat_tracks)
  except:
    return []


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
  return glob(os.path.join(MUSIC_LIB_DIR, '*.mp3'))