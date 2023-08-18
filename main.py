from test.mongo  import Mongo
from test.mqtt  import MQTT
# from signal import pause


mongo = Mongo()
mqtt = MQTT(mongo)

mongo.connect()
mqtt.run()
print("tyfivyv")

# try:
#     pause()
# except KeyboardInterrupt:
#     pass

mqtt.stop()
mongo.disconnect()