import argparse
import tornado.ioloop
import tornado.web
from datetime import datetime
import os
from operator import itemgetter
import requests
from time import sleep

# SBrick
from lib.sbrick_m2mipc import SbrickIpcClient
sbrickid = '88:6B:0F:43:A9:35'
# MQTT connect
client = SbrickIpcClient(broker_ip='127.0.0.1', broker_port=1883)
client.connect()

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
        speed = self.settings['speed']
        if '37' in command:
            motor.forward_left(speed)
        elif '38' in command:
            motor.forward(speed)
        elif '39' in command:
            motor.forward_right(speed)
        elif '40' in command:
            motor.backward(100)
        elif '87' in command:
            motor.arm_up(speed)
        elif '83' in command:
            motor.arm_down(speed)
        elif '65' in command:
            motor.angle_up(speed)
        elif '68' in command:
            motor.angle_down(speed)
        
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

    def __init__(self, pinForward, pinBackward, pinControlStraight,pinLeft, pinRight, pinControlSteering):
        """ Initialize  """
        self.pinForward = pinForward
        self.pinBackward = pinBackward
    
    def angle_up(self, speed):
        client.publish_drive(sbrick_id=sbrickid, channel='02', direction='01', power='f0', exec_time=2)
    
    def angle_down(self, speed):
        client.publish_drive(sbrick_id=sbrickid, channel='02', direction='00', power='f0', exec_time=2)
    
    def arm_up(self, speed):
        client.publish_drive(sbrick_id=sbrickid, channel='03', direction='00', power='f0', exec_time=2)

    def arm_down(self, speed):
        client.publish_drive(sbrick_id=sbrickid, channel='03', direction='01', power='f0', exec_time=2)

    def forward(self, speed):
        client.publish_drive(sbrick_id=sbrickid, channel='01', direction='00', power='f0', exec_time=2)

    def forward_left(self, speed):
        client.publish_drive(sbrick_id=sbrickid, channel='01', direction='00', power='f0', exec_time=2)
        client.publish_drive(sbrick_id=sbrickid, channel='00', direction='00', power='f0', exec_time=2)

    def forward_right(self, speed):
        client.publish_drive(sbrick_id=sbrickid, channel='01', direction='00', power='f0', exec_time=2)
        client.publish_drive(sbrick_id=sbrickid, channel='00', direction='01', power='f0', exec_time=2)

    def backward(self, speed):
        client.publish_drive(sbrick_id=sbrickid, channel='01', direction='01', power='f0', exec_time=2)

    def left(self, speed):
        client.publish_drive(sbrick_id=sbrickid, channel='00', direction='00', power='f0', exec_time=1)

    def right(self, speed):
        client.publish_drive(sbrick_id=sbrickid, channel='00', direction='01', power='f0', exec_time=1)

    def stop(self):
        client.publish_drive(sbrick_id=sbrickid, channel='01', direction='01', power='f0', exec_time=0.1)

def make_app(settings):
    return tornado.web.Application([
        (r"/drive",MultipleKeysHandler),(r"/post", PostHandler, {'settings':settings}),
        (r"/StoreLogEntries",StoreLogEntriesHandler)
    ])

if __name__ == "__main__":

    # Parse CLI args
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--speed_percent", required=True, help="Between 0 and 100")
    args = vars(ap.parse_args())
    motor = Motor(16, 18, 22, 19, 21, 23)
    log_entries = []
    settings = {'speed':float(args['speed_percent'])}
    app = make_app(settings)
    app.listen(81)
    tornado.ioloop.IOLoop.current().start()
