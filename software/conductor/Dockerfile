FROM  balenalib/rpi-raspbian:latest
#FROM balenalib/raspberrypi4-64-debian:latest
#FROM balenalib/raspberrypi4-64-debian-python:latest

WORKDIR /conductor
COPY . .

RUN [ "cross-build-start" ]
RUN install_packages \
    build-essential \
    python3 \
    python3-pip \
    python3-numpy \
    libatlas3-base \
    ffmpeg \
    omxplayer
    
RUN pip3 install --no-cache-dir -r requirements.txt
RUN [ "cross-build-end" ]


ENV UDEV=1

CMD ["python3", "./conductor.py"]