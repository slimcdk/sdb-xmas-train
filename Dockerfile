FROM python:3.7


# install dependencies
RUN apt-get update && apt upgrade -y
RUN apt-get install ffmpeg libavcodec-extra -y
RUN pip install pyserial pydub RPi.GPIO
