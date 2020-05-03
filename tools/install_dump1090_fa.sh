#!/usr/bin/env bash
echo "############## Install Dependecies ######################"
sudo apt-get install build-essential debhelper librtlsdr-dev pkg-config dh-systemd libncurses5-dev libbladerf-dev cowsay >> build.log
sudo apt-get install librtlsdr-dev >> build.log
sudo apt-get install git >> build.log
echo "############## Dowload REPO ######################"
git clone https://github.com/flightaware/dump1090.git >> build.log
cd dump1090
echo "############## Building dump1090 ######################"
make BLADERF=no >> build.log
echo "############## COMPLETE ##################"
cowsay "Yeee Haa! Installation complete!"
echo "now run: ./dump1090/dump1090 --net --fix --fix --modeac --gain 49.6"
echo "See also: --no-crc-check  with ./dump1090/dump1090 --help"
