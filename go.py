from lib.sbrick_m2mipc import SbrickIpcClient
sbrickid = '88:6B:0F:43:A9:35'
# MQTT connect
client = SbrickIpcClient(broker_ip='127.0.0.1', broker_port=1883)
client.connect()

# Get voltage and temperature of a SBrick device
json_response = client.rr_get_adc(sbrick_id=sbrickid, timeout=5)

# output json_response

# Get information of UUID, sercies and characteristics of a SBrick device
json_response = client.rr_get_service(sbrick_id=sbrickid, timeout=5)

# Get general information of a SBrick device
json_response = client.rr_get_general(sbrick_id=sbrickid, timeout=5)

# Stop power functions
# client.publish_stop(sbrick_id=sbrickid, channel_list=['00', '01'])

# Drive a power function
# 00 00 vehicle goes left
# 00 01 vehicle goes right
# 01 00 vehicle forwards
# 01 01 vehicle reverses
# 02 00 arm orients down
# 02 01 arm orients up
# 03 00 arm goes up
# 03 01 arm goes down
client.publish_drive(sbrick_id=sbrickid, channel='01', direction='00', power='f0', exec_time=2)
client.publish_drive(sbrick_id=sbrickid, channel='03', direction='00', power='f0', exec_time=4)
client.publish_drive(sbrick_id=sbrickid, channel='02', direction='01', power='f0', exec_time=2)

# MQTT disconnect
client.disconnect()