import time
import RPi.GPIO as GPIO
import subprocess as sp 
import threading
import thread
import sqlite3
from datetime import datetime
import paho.mqtt.client as mqtt


GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("PBL")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if(str(msg.payload)=='0'):
        GPIO.output(22,0)
    elif(str(msg.payload)=='1'): 
        GPIO.output(22,1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
