#!/usr/bin/python3
"""
buzzer_HackCCM.py

Just a buzzer, with a disable/enable button, that receives messages fro MQTT

Created on Fri Apr 27 12:02:54 2018

@author: msydor
"""

import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

PIN_BUZZ = 21
PIN_SWITCH = 13

broker_address='192.168.0.54'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)    # GPIO.BOARD | GPIO.BCM
#GPIO.setmode(GPIO.BOARD)    # GPIO.BOARD | GPIO.BCM

# set up the SPI interface pins 
GPIO.setup(PIN_BUZZ,   GPIO.OUT)
GPIO.setup(PIN_SWITCH, GPIO.IN)

global ACTIVE   # state of the buzzer
global MOTION   # if motion was detected
global DEBOUNCE # software debouncing of the switch

ACTIVE   = False
MOTION   = False
DEBOUNCE = False

def lightSleep( delay ):
    for i in range(0, int(delay*10 )):
        time.sleep(0.1)

def alert():
    global MOTION                   # reset MOTION here...
    global DEBOUNCE                 # rearm DEBOUNCE here...
    print('alerting...')
    for i in range(4):
        GPIO.output(PIN_BUZZ, True)
        lightSleep(0.25)
        GPIO.output(PIN_BUZZ, False)
        lightSleep(0.5)
    MOTION = False
    DEBOUNCE = False
        
def h_switch(PIN_SWITCH):          # switch callback
    global MOTION 
    global ACTIVE
    global DEBOUNCE
    
    print('h_switch::got SWITCH event')
    
    if( not DEBOUNCE ):
        DEBOUNCE = True
        if( MOTION ):
            print('Changing MOTION state...')
            ACTIVE = not ACTIVE                   # enable BUZZER 
            if( ACTIVE ):
                print('Buzzer ACTIVE')
            else:
                print('Buzzer DISABLED')
        else:
            print('debouncing in effect')
            print('Changing MOTION state...')
            ACTIVE = not ACTIVE                   # enable BUZZER 
            if( ACTIVE ):
                print('Buzzer ACTIVE')
            else:
                print('Buzzer DISABLED')
        
def on_connect(client, userdata, flags, rc):
 
    global CONNECTED
    if rc == 0:
 
        print("BUZZER:: Connected to broker")
        CONNECTED = True
 
    else:
        print("BUZZER:: Connection failed")
        
    return
 
def on_message(client, userdata, message):
    
    global MOTION
    global ACTIVE
    global DEBOUNCE
    
    print( "BUZZER:: Message received: "  + str(message.payload.decode("utf-8")) )
    MOTION = True
    DEBOUNCE = False
   
    if((message.payload.decode("utf-8") == 'EVENT') and ACTIVE):
        print('Emitting buzzer')
        alert()
    else:
        print('ignoring event...')
    
    return


global CONNECTED
CONNECTED = False

GPIO.add_event_detect(PIN_SWITCH, GPIO.RISING) 
GPIO.add_event_callback(PIN_SWITCH, h_switch) 
    


#create new instance
#
client = mqtt.Client('buzzer') 

#connect to broker
#
client.connect(broker_address) 

client.on_connect= on_connect
client.on_message= on_message
 
 
client.loop_start()
 
while CONNECTED != True:
    lightSleep(0.1)
 
client.subscribe("pcam/motion")

# spin, wiating for messages
#
try:
    while True:
        lightSleep(1)
 
except KeyboardInterrupt:
    print ("exiting")

# clean up
#
client.disconnect()
client.loop_stop()
