# aws-iot-mqttlib
python lib to make mqtt connections simpler

(awsiotmqttlib.py)

I made this code, because I was shocked that there doesnt seem to be any
pre-written direct AWS IoT code to make it easier to get started with
AWS IoT

Right now, the library only provides a single function, 
create_iot_connection()

Details of the connection are sorted out through the
awsiotmqttlib-config.yaml
file

## Demo

A trivial little demo is included.

It calls the create_iot_connection() function, and then 
proceeds to first subscribe to a dummy topic, publish to
that topic, and then as validation, print out the same mesage
that it received back from AWS IoT MQTT

## Requirements

1. A valid set of AWS IoT "thing" certs that have iot permissions

2. The awsiotsdk python pip installed
(do   pip3 -r requirements.txt )
