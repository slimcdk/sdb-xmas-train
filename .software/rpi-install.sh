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
echo Upgrading system
apt update
apt upgrade -y


## USBMOUNT
# https://raspberrypi.stackexchange.com/questions/100312/raspberry-4-usbmount-not-working
echo Installing USB mount
sed -i 's/PrivateMounts=yes/PrivateMounts=no/g' /lib/systemd/system/systemd-udevd.service


## RTC MODULE
# https://www.raspberrypi-spy.co.uk/2015/05/adding-a-ds3231-real-time-clock-to-the-raspberry-pi/
apt install i2c-tools
#echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
#hwclock -s


## DOCKER
echo Installing Docker
apt install docker -y
usermod -aG docker $USER



## REPO
echo Getting git and train source code
apt install git git-core -y
git clone https://github.com/slimcdk/sdb-xmax-train
cd sdb-xmas-train


# ADAFRUIT READ ONLY OS
#wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/read-only-fs.sh
#bash read-only-fs.sh

echo Done. You should now reboot
