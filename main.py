#!/usr/bin/python
import sys
import time
import board
import random
from paho.mqtt import client as mqtt_client
from adafruit_seesaw.seesaw import Seesaw
import yaml

with open('config.yml', 'r') as file:
    mqttServer = yaml.safe_load(file)

broker = mqttServer['mqtt']['broker']
port = int(mqttServer['mqtt']['port'])
username = mqttServer['mqtt']['username']
password = mqttServer['mqtt']['password']

#MQTT topic and client ID
topicTemp = "shed/seesaw/temperature"
topicMoisture = "shed/seesaw/moisture"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
#Set up the moisture sensor
i2c_bus = board.I2C()
ss = Seesaw(i2c_bus, addr=0x36)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        try:
            moisture = ss.moisture_read()
            temperature = ss.get_temp()
            rounded_temp = round(temperature, 1)
            result = client.publish(topicTemp, rounded_temp)
            result = client.publish(topicMoisture, moisture)
            print(f"Send `{topicTemp}` to topic `{topicTemp}`")
        except RuntimeError as error:
            #print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            raise error
        time.sleep(15)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()




