# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client
from datetime import datetime
import json


broker = 'broker.emqx.io' # Broker name
port = 1883 # Port number of broker
topic = "python/mqtt" # Topic for publishing or subscriping
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        #msg = f"messages: {msg_count}"
        msg = json.dumps({"sensor_id":random.randint(1,1000),"value":random.randint(1,10000),"timestamp":str(datetime.now())})
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 2000:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
