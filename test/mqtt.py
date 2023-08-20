import os
import logging

import paho.mqtt.client as mqtt
from .mongo import Mongo

from .exception import log_errors

# Creating an object
logger = logging.getLogger()


MQTT_BROKER = "broker.emqx.io" #"127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 6000
MQTT_QOS = 2
MQTT_TOPICS = ("python/#")  # Array of topics to subscribe; '#' subscribe to ALL available topics

MQTT_BROKER = os.getenv("MQTT_BROKER", MQTT_BROKER)
MQTT_PORT = os.getenv("MQTT_PORT", MQTT_PORT)
MQTT_KEEPALIVE = os.getenv("MQTT_KEEPALIVE", MQTT_KEEPALIVE)
MQTT_QOS = os.getenv("MQTT_QOS", MQTT_QOS)
MQTT_TOPICS = os.getenv("MQTT_TOPICS", MQTT_TOPICS)  # As ENV, comma separated
if isinstance(MQTT_TOPICS, str):
    MQTT_TOPICS = [e.strip() for e in MQTT_TOPICS.split(",")]


class MQTT(object):
    """Mqtt subscriber"""
    def __init__(self, mongo: Mongo):
        self.mongo: Mongo = mongo
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
       

    # noinspection PyUnusedLocal
    @staticmethod
    @log_errors
    def on_connect(client: mqtt.Client, userdata, flags, rc):
        logger.info("Connected MQTT")
        for topic in MQTT_TOPICS:
            client.subscribe(topic, MQTT_QOS)

    # noinspection PyUnusedLocal
    @log_errors
    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        """Save the data in mongobd on message received."""
        logger.info("Rx MQTT")
        self.mongo.save(msg)
        self.mongo.retrive_the_data()

    @log_errors
    def run(self):
        """run the mqtt server"""
        logger.info("Running MQTT")
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        self.mqtt_client.loop_forever()

    @log_errors
    def stop(self):
        """For stop the mqtt"""
        logger.info("Stopping MQTT")
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
