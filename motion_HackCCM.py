#!/usr/bin/python3
"""

Motion only routine to message a buzzer

Created on Fri Apr 27 11:55:45 2018

@author: msydor
"""

# Operating States...
#
MOTION        = False         # cotrols the time-lapse loop

# Motion Sensor location
#
PIN_MOTION = 4

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import signal
import time

global ACTIVE
ACTIVE = False

def lightSleep( delay ):
    for i in range(0, int(delay*10 )):
        time.sleep(0.1)

def h_signal(signum, frame):

    global ACTIVE
    global MOTION

    
    if ( signum == signal.SIGQUIT):
        print('h_signal::Shutdown signal received')
        MOTION = False
        
    signal.alarm(0)                 # clear alarm state    
    
def h_active(PIN_MOTION):          # sensor callback
    global MOTION  
    print('h_active::got MOTION event') 
    MOTION = True                   # enable MOTION loop
    
    client.publish("pcam/motion","EVENT")
    
    # BLOCK for 5 seconds, so as not to annoy the receiver
    time.sleep(5)


    
def on_connect(client, userdata, flags, rc):
    
    global CONNECTED
 
    if rc == 0:
 
        print("MOTION::Connected to broker")
 
        global Connected                #Use global variable
        CONNECTED = True                #Signal connection 
 
    else:
 
        print("MOTION::Connection failed")
       

        
# GPIO setup
#
#GPIO.cleanup(PIN_MOTION)

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)    # GPIO.BOARD | GPIO.BCM


GPIO.setup(PIN_MOTION, GPIO.IN)         #Read output from PIR motion sensor
GPIO.add_event_detect(PIN_MOTION, GPIO.RISING) 
GPIO.add_event_callback(PIN_MOTION, h_active) 

#PLATFORM = os.getenv('PCAM_NAME')
#broker_address=os.getenv('MQ_BROKER')
broker_address = '192.168.0.54'

#create new instance
#
client = mqtt.Client("picam") 

#connect to broker
#
print('MOTION:: broker address:', broker_address)
client.connect(broker_address) 
client.on_connect= on_connect                      #attach function to callback

client.loop_start()        #start the messaging loop
 
while CONNECTED != True:    #Wait for connection
    lightSleep(0.2)

while CONNECTED:         # Main Event loop - waiting for motion
    lightSleep(5)
    MOTION = False

client.disconnect()