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

## See also

https://repost.aws/knowledge-center/iot-core-publish-mqtt-messages-python

gives some manual details of how to create a test "thing", etc.

If requested, I might create scripts to do that for people.

Additionally, there is a related "workshop" at
https://catalog.us-east-1.prod.workshops.aws/workshops/7c2b04e7-8051-4c71-bc8b-6d2d7ce32727/en-US/thing-groups/static-thing-groups
