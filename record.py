from __future__ import division

import picamera
import numpy as np
from datetime import datetime
import os

motion_dtype = np.dtype([
    ('x', 'i1'),
    ('y', 'i1'),
    ('sad', 'u2'),
    ])


file_path = str(os.path.dirname(os.path.realpath(__file__)))+"/video_timestamps.txt"

class MyMotionDetector(object):
    def __init__(self, camera):
        width, height = camera.resolution
        self.cols = (width + 15) // 16
        self.cols += 1 # there's always an extra column
        self.rows = (height + 15) // 16

    def write(self, s):
        # Load the motion data from the string to a numpy array
        data = np.fromstring(s, dtype=motion_dtype)
        # Re-shape it and calculate the magnitude of each vector
        data = data.reshape((self.rows, self.cols))
        data = np.sqrt(
            np.square(data['x'].astype(np.float)) +
            np.square(data['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 60, then say we've detected motion
        if (data > 60).sum() > 10:
            print('Motion detected!')
        # record timestamp data
        timestamp = datetime.now()
        with open(file_path,"a") as writer:
            writer.write(str(timestamp)+"\n")
        # Pretend we wrote all the bytes of s
        return len(s)

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 10
    camera.start_recording(
        # Throw away the video data, but make sure we're using H.264
        'raspcamera_feed.h264', format='h264',
        # Record timestamp data to our custom output object
        motion_output=MyMotionDetector(camera)
        )
    camera.wait_recording(1000)
    camera.stop_recording()