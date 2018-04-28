#!/bin/sh
#
# setup a raspberry pi for HackCCM, camera and messaging tutorials

# assuming unknown state
#
sudo apt-get install git-core
sudo apt-get install python3-picamera 
sudo apt-get install python3-pip

# assuming NOOBS distribution
#
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install libav-tools
sudo apt-get install x264
sudo apt-get install realvnc-vnc-server
sudo systemctl enable vncserver-x11-serviced.service
sudo pip3 install paho-mqtt

sudo apt-get install realvnc-vnc-server
sudo apt-get install realvnc-vnc-viewer
sudo systemctl enable vncserver-x11-serviced.service



