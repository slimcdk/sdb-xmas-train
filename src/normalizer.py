#!/usr/bin/python3

import os, shutil
from glob import glob
from pydub import AudioSegment

from musician import *
from utils import *

MUSIC_LIB_PATH = '/music'

target_gain = -20



def normalize_tracks():

  playlist = get_full_playlist()
  print('Found {} tracks to be normalized to {} db'.format(len(playlist), target_gain))

  # Rename tracks
  for track in get_full_playlist():
    new_name = track.replace(" ", ".").replace("-","").replace("..", ".")
    os.rename(os.path.join(get_vault_path(), track), os.path.join(get_vault_path(), new_name))
    
  # Adjust gain
  for track in get_full_playlist():
    try:
      sound = AudioSegment.from_file(os.path.join(MUSIC_LIB_PATH, track), 'mp3')
      normalized_track = match_target_amplitude(sound, target_gain)
      normalized_track.export(os.path.join(MUSIC_LIB_PATH, track), format='mp3')
      print(f'Succeded to normalize: {track}')

    except Exception:
      print(f'Failed to normalize: {track}')



normalize_tracks()



def match_target_amplitude(track, target_dbfs):
  change_in_dbfs = target_dbfs - track.dBFS
  return track.apply_gain(change_in_dbfs)
