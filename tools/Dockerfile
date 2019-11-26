FROM balenalib/rpi-raspbian


RUN apt-get update -y
RUN apt-get -y install libatlas3-base ffmpeg
RUN apt-get -y install python3.7 python3-pip

# install Python modules
RUN pip3 install -U pydub


COPY normalize_playlist.py /sdb-train/normalize_playlist.py
#COPY /media/usb /sdb-train/music

WORKDIR /sdb-train
CMD python3 /sdb-train/normalize_playlist.py
