# SBrickPy
This is a python based interface to control RC hobby car, typically those under the label "RTR" or Ready To Run, and ultimately mhake them autonomous with a webcam.
  
The raspberry pi will send pulses on its GPIO pins, allowing different speeds and anglesd

Todos:
* Main car. Equivalent to main robot loader/builder/truck/renovator IRL
  * (done) Show voltage and temperature
  * Add variable speed, with cursor command on page
  * Add httpauth, dynamicdns with access from outside network
  * Add removable actuator to front: loader, wallet transport, welding, 3-degree robot arm, sensor (soil humidity)
  * Use USB controller (Playstation, XBox) to drive (optional)
* Camera sensor:
  * Add a combination of LIDAR fixed cam and a m4/3 Z-CAM E1 camera with pan/tilt as secondary large sensor camera. Use RC battery to power. Use FPV hmdi converter to feed video
  * Add face recognition to main camera. Stop robot if recognize. Open door for delivery if authorized.
  * Add HDR+ to main camera http://timothybrooks.com/tech/hdr-plus/
* Indoor positioning system with cameras placed on ceiling, car with "QR Code". Equivalent to a drone IRL
  * Add pathing A to B
* Protected Garage with wireless charging. Equivalent to a base IRL

## Requirements
* Python 3.4

## Prerequesites
```bash
$ ping raspberrypi.local
```
# And you should see results like this:
PING raspberrypi.local (192.168.1.11): 56 data bytes
64 bytes from 192.168.1.11: icmp_seq=0 ttl=64 time=12.195 ms
64 bytes from 192.168.1.11: icmp_seq=1 ttl=64 time=155.695 ms
64 bytes from 192.168.1.11: icmp_seq=2 ttl=64 time=49.939 ms
64 bytes from 192.168.1.11: icmp_seq=3 ttl=64 time=31.751 ms

Optional: you can choose a raspberry hostname of your preference by editing file:

$ sudo vi /etc/hostname
$ reboot

## Usage

### Start Videofeed

Open a tab
```
$ cd /usr/src/mjpg-streamer/mjpg-streamer-experimental
$ ./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -x 640 -y 480 -fps 20 -ex night"
```
### Learning

Open a third tab to get Raspberry Pi send user commands to SBrick Pi through Bluetooth
```
$ sudo python3 drive_api.py -s 50
```
Open a last tab to record stream and session commands
```
$ sudo python3 record.py
```
Happy driving
