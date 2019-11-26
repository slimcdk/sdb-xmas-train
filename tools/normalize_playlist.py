import os
from glob import glob
from pydub import AudioSegment


MUSIC_LIB_PATH = '/media/usb'
target_gain = -20



def match_target_amplitude(track, target_dBFS):
  change_in_dBFS = target_dBFS - track.dBFS
  return track.apply_gain(change_in_dBFS)

full_path_playlist = glob(os.path.join(MUSIC_LIB_PATH, '*.mp3'))
playlist = [track.replace(MUSIC_LIB_PATH+'/', '') for track in full_path_playlist]
#print([track for track in playlist])


if not os.path.exists(os.path.join(MUSIC_LIB_PATH, 'normalized_tracks')):
  os.mkdir(os.path.join(MUSIC_LIB_PATH, 'normalized_tracks'))


print('Found {} tracks to be normalized with {} db'.format(len(playlist), target_gain))


for track in playlist:

  print('normalizing', track)

  try:
    sound = AudioSegment.from_file(os.path.join(MUSIC_LIB_PATH, track), 'mp3')
    normalized_track = match_target_amplitude(sound, target_gain)

    track_name =  '-'.join([word.lower() for word in track.split(' ')])
    normalized_track.export(os.path.join(MUSIC_LIB_PATH, 'normalized_tracks', track_name), format='mp3')
    print('normaliztion succeeded')

  except:
    print('failed to normalize track', track)
