#!/usr/bin/python3

# To use this code, either copy the file to your code directory,
# and use
#
#   from awsiotmqttlib import create_iot_connection
#
# or keep it someplace common, and use
#
#  if os.path.exists("awsiotmqttlib.py"):
#    exec(open("awsiotmqttlib.py").read())
#
# Then you can use function create_iot_connection()
#
# The code requires:
# 1 
#  A config file formatted as follows:
# ---
# config:
#  certificateFilePath: "/cert.pem"
#  privateKeyPath: "priv.pem"
#  rootCaPath: "rootca.pem"
#  thingName: "awsiotmqttlib-device"
#  awsRegion: "us-west-2"
#  iotDataEndpoint: "az4u3hiaocf2l-ats.iot.us-west-2.amazonaws.com"
# ##################
# "thingName" is just used as "client_id" for mqtt connection builder


import yaml

from awscrt import io, mqtt
from awsiot import mqtt_connection_builder



#############################################################################
# Mostly generic required junk

# Boilerplate for mqtt_connection_builder
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. Error: {}".format(error))

# Boilerplate for mqtt_connection_builder
# Callback when an interrupted connection is re-established
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))
    if (return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present):
        print("Session did not persist Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread
        # Evaluate result with a callback instead
        resubscribe_future.add_done_callback(on_resubscribe_complete)


# Callback to resubscribe to previously subscribed topics upon lost session
# Called only by above on_connection_resumed
def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))
    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))

def get_client_bootstrap():
  event_loop_group = io.EventLoopGroup(1)
  host_resolver = io.DefaultHostResolver(event_loop_group)
  client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
  return client_bootstrap

def create_iot_connection(configfile="awsiotmqttlib-config.yaml"):

  with open(configfile, 'r') as f:
    configdata = yaml.safe_load(f)

  thing_name   = configdata["config"]["thingName"]
  cert_path    = configdata["config"]["certificateFilePath"]
  key_path     = configdata["config"]["privateKeyPath"]
  root_ca_path = configdata["config"]["rootCaPath"]
  endpoint     = configdata["config"]["iotDataEndpoint"]

  if not thing_name:
    print("DEBUG: no thing_name set. Harcoding to demo-device")
    thing_name="demo-device"


  mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=endpoint,
    cert_filepath=cert_path,
    pri_key_filepath=key_path,
    client_bootstrap=get_client_bootstrap(),
    ca_filepath=root_ca_path,
    on_connection_interrupted=on_connection_interrupted,
    on_connection_resumed=on_connection_resumed,
    client_id=thing_name,
    clean_session=True,
    keep_alive_secs=6
  )
  return mqtt_connection

# To see result of connection clearly, use:
# print("connect result=")
# print (mqtt_connection.connect().result())



########################################################
# This "simple" version exists because sometimes, for unclear reasons,
# the nicer fancier one above fails

def create_simple_iot_connection(configfile="awsiotmqttlib-config.yaml"):

  with open(configfile, 'r') as f:
    configdata = yaml.safe_load(f)

  thing_name   = configdata["config"]["thingName"]
  cert_path    = configdata["config"]["certificateFilePath"]
  key_path     = configdata["config"]["privateKeyPath"]
  root_ca_path = configdata["config"]["rootCaPath"]
  endpoint     = configdata["config"]["iotDataEndpoint"]

  if not thing_name:
    print("DEBUG: no thing_name set")
    exit()

  mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=endpoint,
    client_id=thing_name,
    cert_filepath=cert_path,
    pri_key_filepath=key_path,
    ca_filepath=root_ca_path,
    client_bootstrap=get_client_bootstrap()
  )
  return mqtt_connection



