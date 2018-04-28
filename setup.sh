#!/bin/sh

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install libav-tools
sudo apt-get install x264
sudo apt-get install realvnc-vnc-server
sudo systemctl enable vncserver-x11-serviced.service
sudo pip3 install paho-mqtt



