#!/usr/bin/env bash
echo "############## Install Dependecies ######################"
sudo apt-get install build-essential debhelper librtlsdr-dev pkg-config dh-systemd libncurses5-dev libbladerf-dev cowsay >> build.log
sudo apt-get install librtlsdr-dev >> build.log
sudo apt-get install git >> build.log
echo "############## Dowload REPO ######################"
git clone https://github.com/terminator4088/dump1090.git >> build.log
cd dump1090
echo "############## Building dump1090 ######################"
make BLADERF=no >> build.log
echo "############## COMPLETE ##################"
cowsay "Yeee Haa! Installation complete!"
echo "File is auto-copied into ./src folder"
cp dump1090 ../../src
