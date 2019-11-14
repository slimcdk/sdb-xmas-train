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

# UPDATE
apt update
apt upgrade -y


## BINs
apt install git apt-transport-https ca-certificates software-properties-common python3 python3-pip libavcodec-extra ffmpeg usbmount libatlas-base-dev -y


## DOCKER
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
usermod -aG docker $USER


## PYTHON MODULES
pip3 install docker-compose
pip3 install -f requirements.txt


## REPO
git clone git@github.com:slimcdk/sdb-xmas-train.git

## USBMOUNT
# https://raspberrypi.stackexchange.com/questions/100312/raspberry-4-usbmount-not-working
sed -i 's/PrivateMounts=yes/PrivateMounts=no/g' /lib/systemd/system/systemd-udevd.service



# ADAFRUIT READ ONLY OS
#wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/read-only-fs.sh
#bash read-only-fs.sh

