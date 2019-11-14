FROM balenalib/rpi-raspbian


COPY ./software /sdb-train

RUN apt-get update -y
RUN apt-get -y install libatlas3-base
RUN apt-get -y install omxplayer python3.7 python3-pip usbmount 
#python3-numpy

# install Python modules
#RUN pip3 install requirements.txt
RUN pip3 install -U omxplayer-wrapper RPI.GPIO numpy mutagen

VOLUME /media/usb /sdb-train/music

CMD python3 /sdb-train/conductor.py
