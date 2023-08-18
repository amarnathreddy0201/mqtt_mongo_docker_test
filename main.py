import logging
from test.mongo  import Mongo
from test.mqtt  import MQTT

# Create and configure logger
logging.basicConfig(filename="mqtt_mongo_test.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w')
 
# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
 
if __name__ == "__main__":
    logger.info("main function started")
    mongo = Mongo()
    mqtt = MQTT(mongo)

    mongo.connect()
    mqtt.run()
    print("tyfivyv")

    mqtt.stop()
    mongo.disconnect()