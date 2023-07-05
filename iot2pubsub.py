#!/usr/bin/python3

# Super-basic use of my "awsiotmqttlib" routines.
# 1. Subscribe to a topic
# 2. repeatedly publish a new integer to the topic
# 2.1 print out the published message once we receive it back through MQTT

import time

exec(open("awsiotmqttlib.py").read())

TESTTOPIC = "dt/test/subtopic"

def testpublish(message):
    mqtt_connection.publish(
      topic=TESTTOPIC ,
      payload=message,
      qos=mqtt.QoS.AT_LEAST_ONCE)

# Receive data from topic subcription
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    if topic.endswith(TESTTOPIC):
        #print(payload.decode('utf-8'))
        #savedeviceshadow(payload.decode('utf-8'))
        print("Current topic value: " + payload.decode('utf-8'))
    else:
        print("Unrecognized topic received: " + topic)


mqtt_connection = create_iot_connection()


# Connect to the AWS IoT endpoint
print("connect result=")
print (mqtt_connection.connect().result())


def subscribe_topic(message_topic):
    print("Subscribing to topic '{}'...".format(message_topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
      topic=message_topic,
      qos=mqtt.QoS.AT_LEAST_ONCE,
      callback=on_message_received)
    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))


subscribe_topic(TESTTOPIC)

counter=1
# publish to topic which we also read back ourselves
while True:
    testpublish(str(counter))
    counter=counter + 1
    time.sleep(2)


