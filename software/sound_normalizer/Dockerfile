FROM balenalib/rpi-raspbian


RUN apt-get update -y
RUN apt-get -y install libatlas3-base ffmpeg
RUN apt-get -y install python3.7 python3-pip

RUN pip3 install -U pydub

COPY normalizer.py /sdb-train/normalizer.py

WORKDIR /sdb-train
CMD python3 /sdb-train/normalizer.py