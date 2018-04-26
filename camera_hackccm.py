#!/usr/bin/python3
#
# camera_hackccm.py - capturing still images
#
# create a directory with a timestamp and put (5) images, 2 seconds delay,
# into that directory.  Do some logging and build a metadata file for each
# event that triggers a TimeLapse session, in that same directory
#
##############################################################
# make sure to disable RPi-Cam-Web before using this program #
##############################################################




import picamera
import time
from datetime import datetime
import os
#import logging
#import logging.config

# Duration of image capture (sec)
_DURATION = 2*60

# Location of Time Lapse Capture Directory
_IMAGE_DIR = '/home/pi/TimeLapse'

# Camera identifer (prefix to image filename and clapboard
_CAMERA = 'picam1'

# Time laspe interval in (sec)
_DELAY = 2

# Collect images for 2 minutes
_IMAGES_TO_CAPTURE = _DURATION/_DELAY

# File extension to use
_FILE_TYPE = '.jpg'

def createAndOpenDir( path):

        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        dirname = path + '/' + _CAMERA + '_' + now
        
        # create the directory
        os.mkdir(dirname)
        
        return dirname

def createTimeStampName():

        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = now + _FILE_TYPE
        
        return filename
#
# Setup metadata file, for each event
#

#
# Setup logging file, roll over every 7 days << setup in *.ini file
#
#logging.config.fileConfig('camera_log_config.ini')
#logger = logging.getLogger('camera')

camera = picamera.PiCamera()
imageCount = 0
#logger.info('Beginning TimeLapse session')

try:
	camera.start_preview()
	thisDirectory = createAndOpenDir( _IMAGE_DIR )
	os.chdir( thisDirectory )
#	logger.info('Created directory %s', thisDirectory)

	for i in range(1,5):
		camera.capture( createTimeStampName() )
		imageCount += 1
		time.sleep(_DELAY)
#	logger.info('Captured %s images to %s', imageCount, thisDirectory)

	camera.stop_preview()
finally:
	camera.close()
#	logger.info('Closing session')



