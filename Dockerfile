FROM python:3.7


# install dependencies
RUN apt-get update && apt upgrade -y
RUN apt-get install libavcodec-extra libdbus-1-3 libdbus-1-dev -y

RUN pip install pydub RPi.GPIO mutagen omxplayer-wrapper
