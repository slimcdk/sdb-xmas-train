FROM  balenalib/rpi-raspbian:latest

# Setup
#WORKDIR /app
#COPY requirements.txt .

RUN [ "cross-build-start" ]
#RUN install_packages \
#    build-essential \
#    python3 \
#    python3-pip \
#    python3-numpy \
#    libatlas3-base \
#    ffmpeg

#RUN pip3 install -r requirements.txt
RUN [ "cross-build-end" ]


# App
#COPY normalizer.py .
COPY ./music /music

ENV UDEV=1

#CMD python3 normalizer.py
