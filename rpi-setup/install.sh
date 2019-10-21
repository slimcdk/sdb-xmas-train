#!/bin/bash

###
#
# https://askubuntu.com/questions/20414/find-and-replace-text-within-a-file-using-commands
#
#
###



if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi



## GIT AND REPO
apt install git -y
git clone git@github.com:slimcdk/sdb-xmas-train.git


## PYTHON
apt install python3 python3-pip -y


## OMXPLAYER
apt install  omxplayer -y


## USBMOUNT
# https://raspberrypi.stackexchange.com/questions/100312/raspberry-4-usbmount-not-working
apt install usbmount
sed -i 's/PrivateMounts=yes/PrivateMounts=no/g' /lib/systemd/system/systemd-udevd.service



# ADAFRUIT READ ONLY OS
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/read-only-fs.sh
bash read-only-fs.sh

