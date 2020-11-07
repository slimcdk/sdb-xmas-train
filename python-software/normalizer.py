#!/usr/bin/python3

import os
from glob import glob
from pydub import AudioSegment


print ("PROCESSSING MUSIC")
exit(0)




'''
MUSIC_LIB_PATH = '/music'
NORMALIZED_LIB_DIR = '.normalized_tracks'

target_gain = -20


def match_target_amplitude(track, target_dbfs):
  change_in_dbfs = target_dbfs - track.dBFS
  return track.apply_gain(change_in_dbfs)


# get tracks
full_path_playlist = glob(os.path.join(MUSIC_LIB_PATH, '*.mp3'))
playlist = [track.replace(MUSIC_LIB_PATH+'/', '') for track in full_path_playlist]
print('Found {} tracks to be normalized with {} db'.format(len(playlist), target_gain))

# create directory for exported tracks
if not os.path.exists(os.path.join(MUSIC_LIB_PATH, NORMALIZED_LIB_DIR)):
  os.mkdir(os.path.join(MUSIC_LIB_PATH, NORMALIZED_LIB_DIR))


# do the adjusting for each track
for track in playlist:

  print('normalizing', track, end='')

  try:
    sound = AudioSegment.from_file(os.path.join(MUSIC_LIB_PATH, track), 'mp3')
    normalized_track = match_target_amplitude(sound, target_gain)

    track_name =  '-'.join([word.lower() for word in track.split(' ')])
    normalized_track.export(os.path.join(MUSIC_LIB_PATH, NORMALIZED_LIB_DIR, track_name), format='mp3')
    print('succeeded')

  except:
    print('failed')
    exit(0)


print ('normalizer finished')
exit(0)
'''