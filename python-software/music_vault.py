import os, random
from glob import glob
import numpy as np



last_played_track = None
MUSIC_LIB_DIR = '/music'
if os.path.exists(os.path.join(MUSIC_LIB_DIR, '.normalized_tracks')):
  MUSIC_LIB_DIR = os.path.join(MUSIC_LIB_DIR, '.normalized_tracks')
  print('Found normalized tracks directory ->', MUSIC_LIB_DIR)


def get_sub_playlist(tracks_to_play):
  """returns a playlist fraction"""
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