# Stjær Dagli'Brugsens juletog




### Normalize audio
```bash
$ pip3 install ffmpeg-normalize
$ cd audio
audio$ ffmpeg-normalize -fp -pr --audio-codec libmp3lame -ext mp3 **/*.mp3 --output-folder normalized
```
