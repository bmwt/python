#!/usr/bin/env python3

# note- required lib version 1.2.something, not 1.3
import paho.mqtt.client as mqtt
import configparser
import datetime
import time
from influxdb import InfluxDBClient

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("home/#")

def on_message(client, userdata, msg):
    # Use utc as timestamp
    receiveTime=datetime.datetime.utcnow()
    message=msg.payload.decode("utf-8")
    isfloatValue=False
    try:
        # Convert the string to a float so that it is stored as a number and not a string in the database
        val = float(message)
        isfloatValue=True
    except:
        isfloatValue=False

    if isfloatValue:
        print(str(receiveTime) + ": " + msg.topic + " " + str(val))

        json_body = [
            {
                "measurement": msg.topic,
                "time": receiveTime,
                "fields": {
                    "value": val
                }
            }
        ]

        dbclient.write_points(json_body)

# grab config
config = configparser.ConfigParser()
config.read('/etc/mqtt_to_influxdb.conf')

# Set up a client for InfluxDB
dbclient = InfluxDBClient(config['DEFAULT']['influxdb_host'], 8086, 'mqtt', config['DEFAULT']['influxdb_pwd'], config['DEFAULT']['influxdb_db'])

# Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
connOK=False
while(connOK == False):
    try:
        client.connect(config['DEFAULT']['mqtt_host'])
        connOK = True
    except:
        connOK = False
    time.sleep(2)

# Blocking loop to the Mosquitto broker
client.loop_forever()

