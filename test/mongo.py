from typing import List
from datetime import datetime
import os
import threading
import logging
import json

from .exception import log_errors

import paho.mqtt.client as mqtt
import pymongo
import pymongo.database
import pymongo.collection
import pymongo.errors

logger = logging.getLogger()


MONGO_URI = "mongodb://127.0.0.1:27017"  # mongodb://user:pass@ip:port || mongodb://ip:port
MONGO_DB = "domotics"
MONGO_COLLECTION = "mqtt"
MONGO_TIMEOUT = 1  # Time in seconds
MONGO_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

MONGO_URI = os.getenv("MONGO_URI", MONGO_URI) # mongodb default url
MONGO_DB = os.getenv("MONGO_DB", MONGO_DB) # mongodb creating database
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", MONGO_COLLECTION) # Creating collection name
MONGO_TIMEOUT = float(os.getenv("MONGO_TIMEOUT", MONGO_TIMEOUT))
MONGO_DATETIME_FORMAT = os.getenv("MONGO_DATETIME_FORMAT", MONGO_DATETIME_FORMAT)



class Mongo(object):
    def __init__(self):
        self.client: pymongo.MongoClient = None
        self.database: pymongo.database.Database = None
        self.collection: pymongo.collection.Collection = None
        self.queue: List[mqtt.MQTTMessage] = list()


    @log_errors
    def connect(self):
        """Connecting the mongodb"""
        logger.info("Connecting Mongo")
        self.client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIMEOUT*1000.0)
        self.database = self.client.get_database(MONGO_DB)
        self.collection = self.database.get_collection(MONGO_COLLECTION)
        

    @log_errors
    def disconnect(self):
        logger.info("Disconnecting Mongo")
        if self.client:
            self.client.close()
            self.client = None


    @log_errors
    def connected(self) -> bool:
        if not self.client:
            return False
        try:
            self.client.admin.command("ismaster")
        except pymongo.errors.PyMongoError:
            return False
        else:
            return True


    @log_errors
    def _enqueue(self, msg: mqtt.MQTTMessage):
        logger.info("Enqueuing")
        self.queue.append(msg)
        # TODO process queue


    @log_errors
    def __store_thread_f(self, msg: mqtt.MQTTMessage):
        logger.info("Storing")
        now = datetime.now()
        document =  json.loads(msg.payload.decode())
            # "qos": msg.qos,
            # "timestamp": int(now.timestamp()),
            # "datetime": now.strftime(MONGO_DATETIME_FORMAT),
            # # TODO datetime must be fetched right when the message is received
            # # It will be wrong when a queued message is stored
        
        logger.info(document)
        result = self.collection.insert_one(document)
        logger.info(f"Saved in Mongo document ID - { result.inserted_id}")
        if not result.acknowledged:
            # Enqueue message if it was not saved properly
            self._enqueue(msg)
    

    @log_errors
    def _store(self, msg):
        th = threading.Thread(target=self.__store_thread_f, args=(msg,))
        th.daemon = True
        th.start()


    @log_errors
    def save(self, msg: mqtt.MQTTMessage):
        logger.info("Saving")
        if msg.retain:
            logger.info("Skipping retained message")
            return
        if self.connected():
            self._store(msg)
        else:
            self._enqueue(msg)


    @log_errors
    def retrive_the_data(self):
        """ For fetching the data"""
        for data in self.collection.find({},
            {'_id':0,'sensor_id': 566, 'value': 2973, 'timestamp': '2023-08-20 19:01:39.763867'}): # _id : 0 represents no need to print id value.
            print(data)
        else:
            print("No data present")