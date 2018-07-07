#!/usr/bin/env python

# drives RC car with receiver, servo and brushed motor

import argparse
import tornado.ioloop
import tornado.web
from datetime import datetime
import os
import RPi.GPIO as GPIO
from operator import itemgetter
import requests
import time
from time import sleep

class PostHandler(tornado.web.RequestHandler):

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self,settings):
        self._settings = settings

    def initialize(self, settings):
        self.settings = settings

    def post(self):
        timestamp = datetime.now()
        data_json = tornado.escape.json_decode(self.request.body)
        allowed_commands = set(['37','38','39','40', '87', '65', '83', '68'])
        command = data_json['command']
        command = list(command.keys())
        command = set(command)
        command = allowed_commands & command
        file_path = str(os.path.dirname(os.path.realpath(__file__)))+"/session.txt"
        log_entry = str(command)+" "+str(timestamp)
        log_entries.append((command,timestamp))
        with open(file_path,"a") as writer:
            writer.write(log_entry+"\n")
        print(log_entry)
        speed = str(self.settings['speed'])
        if '37' in command:
            motor.forward_left(speed)
        elif '38' in command:
            motor.forward(speed)
        elif '39' in command:
            motor.forward_right(speed)
        elif '40' in command:
            motor.backward(speed)
        else:
            motor.stop()
        
# This only works on data from the same live python process. It doesn't 
# read from the session.txt file. It only sorts data from the active
# python process. This is required because it reads from a list instead
# of a file  on data from the same live python process. It doesn't 
# read from the session.txt file. It only sorts data from the active
# log_entries python list
class StoreLogEntriesHandler(tornado.web.RequestHandler):
    def get(self):
        file_path = str(os.path.dirname(os.path.realpath(__file__)))+"/clean_session.txt"
        sorted_log_entries = sorted(log_entries,key=itemgetter(1))
        prev_command = set()
        allowed_commands = set(['38','37','39','40'])
        for log_entry in sorted_log_entries:
            command = log_entry[0]
            timestamp = log_entry[1]
            if len(command ^ prev_command) > 0:
                prev_command = command
                with open(file_path,"a") as writer:
                    readable_command = []
                    for element in list(command):
                        if element == '37':
                            readable_command.append("left")
                        if element == '38':
                            readable_command.append("up")
                        if element == '39':
                            readable_command.append("right")
                        if element == '40':
                            readable_command.append("down")
                    log_entry = str(list(readable_command))+" "+str(timestamp)
                    writer.write(log_entry+"\n")
                print(log_entry)
        self.write("Finished")

class MultipleKeysHandler(tornado.web.RequestHandler):

    def get(self):
        print("Hello SBrickers!")
        self.render('index.html')


class Motor:

    def __init__(self, pinControlSteering, pinForward):
        """ Initialize  """
        self.pinControlSteering = pinControlSteering
        GPIO.setup(self.pinControlSteering, GPIO.OUT)
        self.pwm_steering = GPIO.PWM(self.pinControlSteering, 50)
        self.pwm_steering.start(7.5)
        
        self.pinForward = pinForward
        GPIO.setup(self.pinForward, GPIO.OUT)
        self.pwm_forward = GPIO.PWM(self.pinForward, 100)
        self.pwm_forward.start(0)

    def forward(self, speed):
        """ pinForward is the forward Pin, so we change its duty
             cycle according to speed. """
        self.pwm_steering.ChangeDutyCycle(7.5)   
        self.pwm_forward.ChangeDutyCycle(99)
        time.sleep(0.2)  
        self.pwm_forward.ChangeDutyCycle(0)

    def forward_left(self, speed):
        """ pinForward is the forward Pin, so we change its duty
             cycle according to speed. """
        self.pwm_steering.ChangeDutyCycle(2.5)  
        self.pwm_forward.ChangeDutyCycle(99)  
        time.sleep(0.2)    
        self.pwm_steering.ChangeDutyCycle(7.5)  
        self.pwm_forward.ChangeDutyCycle(0)  
        time.sleep(0.02)  

    def forward_right(self, speed):
        """ pinForward is the forward Pin, so we change its duty
             cycle according to speed. """
        self.pwm_steering.ChangeDutyCycle(12.5)     
        self.pwm_forward.ChangeDutyCycle(99)  
        time.sleep(0.2)  
        self.pwm_steering.ChangeDutyCycle(7.5)  
        self.pwm_forward.ChangeDutyCycle(0)  
        time.sleep(0.02) 

    def backward(self, speed):
        """ pinBackward is the forward Pin, so we change its duty
             cycle according to speed. """
        self.pwm_steering.ChangeDutyCycle(7.5)     
        self.pwm_forward.ChangeDutyCycle(0)  

    def left(self, speed):
        """ pinForward is the forward Pin, so we change its duty
             cycle according to speed. """
        self.pwm_steering.ChangeDutyCycle(2.5)   

    def right(self, speed):
        """ pinForward is the forward Pin, so we change its duty
             cycle according to speed. """
        self.pwm_steering.ChangeDutyCycle(12.5)    

    def stop(self):
        """ Set the duty cycle of both control pins to zero to stop the motor. """
        self.pwm_steering.ChangeDutyCycle(7.5)  
        self.pwm_forward.ChangeDutyCycle(99)  
 

def make_app(settings):
    return tornado.web.Application([
        (r"/drive",MultipleKeysHandler), 
        (r"/post", PostHandler, {'settings':settings}),
        (r"/StoreLogEntries",StoreLogEntriesHandler)
    ])

if __name__ == "__main__":

    # Parse CLI args
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--speed_percent", required=True, help="Between 0 and 100")
    args = vars(ap.parse_args())
    GPIO.setmode(GPIO.BOARD)
    motor = Motor(12, 35)
    log_entries = []
    settings = {
        'speed':(args['speed_percent'])
        }
    app = make_app(settings)
    app.listen(81)
    tornado.ioloop.IOLoop.current().start()
