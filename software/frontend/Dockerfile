#FROM balenalib/raspberrypi4-64-alpine-python:3-latest
FROM  balenalib/rpi-raspbian:latest

# Setup
WORKDIR /app
COPY . .

RUN [ "cross-build-start" ]
RUN install_packages \
    build-essential \
    python3 \
    python3-pip
    
RUN pip3 install -r requirements.txt
RUN [ "cross-build-end" ]

# App

#CMD python3 server.py