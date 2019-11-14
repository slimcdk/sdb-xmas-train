FROM python:3.7

WORKDIR .

#RUN DEBIAN_FRONTEND=noninteractive 
#UN apt-get -yq install omxplayer

# install dependencies
RUN apt-get update && apt upgrade -y
RUN apt-get update -y && apt-get -y install wget ca-certificates libpcre3 libfreetype6 fonts-freefont-ttf dbus libssl1.0.0 libsmbclient libssh-4 fbset libraspberrypi0 && wget https://archive.raspberrypi.org/debian/pool/main/o/omxplayer/omxplayer_0.3.6~git20160102~f544084_armhf.deb && dpkg -i  omxplayer_0.3.6~git20160102~f544084_armhf.deb
RUN apt-get install git git-core libavcodec-extra libdbus-1-3 libdbus-1-dev libatlas-base-dev libpcre3 fonts-freefont-ttf fbset libasound2-dev libidn11-dev libboost-dev libssh-dev libsmbclient-dev -y
#  libva1 libssl1.0-dev
#RUN git clone https://github.com/popcornmix/omxplayer.git
#RUN cd omxplayer && chmod +x prepare-native-raspbian.sh && ./prepare-native-raspbian.sh
#RUN make ffmpeg && make -j${nproc}
#RUN make install

RUN pip install RPi.GPIO mutagen omxplayer-wrapper numpy
