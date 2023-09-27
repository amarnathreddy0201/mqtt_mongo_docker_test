# Import the required modules
import mysql.connector
import base64
from PIL import Image
import io
import cv2
import base64
import numpy as np
 
# For security reasons, never expose your password
password = open('password','r').readline()
 
# Create a connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="studentdb"  # Name of the database
)
 
# Create a cursor object
cursor = mydb.cursor()
 
# Prepare the query
query = 'SELECT PICTURE FROM PROFILE'
 
# Execute the query to get the file
cursor.execute(query)
 
data = cursor.fetchall()
for d in data:
    bas64 = base64.b64decode(d[0])

    # Convert the decoded data to a NumPy array
    image_array = np.frombuffer(bas64, np.uint8)

    # Decode the image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    

    cv2.imshow("image",image)
    cv2.waitKey(0)
    