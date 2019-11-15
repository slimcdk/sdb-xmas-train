FROM balenalib/rpi-raspbian


RUN apt-get update -y
RUN apt-get -y install libatlas3-base
RUN apt-get -y install omxplayer python3.7 python3-pip usbmount python3-numpy

# install Python modules
RUN pip3 install -U omxplayer-wrapper RPI.GPIO mutagen

#VOLUME /sdb-train
#VOLUME /media/usb /sdb-train/music


COPY software/conductor.py /sdb-train/conductor.py

WORKDIR /sdb-train
CMD python3 /sdb-train/conductor.py
