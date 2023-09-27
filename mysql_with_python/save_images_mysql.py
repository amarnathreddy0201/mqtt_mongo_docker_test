# Import the required modules
import mysql.connector
import base64
from PIL import Image
import io
import cv2
import glob
import random


images = glob.glob("D:/Family/*.jpg")





# For security reasons, never expose your password
password = open('password','r').readline() # Create password file and write your mysql password and readline.

# Create a connection
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password=password,
	database="studentdb" # Name of the database
)

# Create a cursor object
cursor = mydb.cursor()


final_data =[]
for i,dat in enumerate(images):
    image = cv2.imread(dat,1)
    _,im_arr = cv2.imencode('.jpg', image)  # im_arr: image in Numpy one-dim array format.
   
    file = base64.b64encode(im_arr)
    final_data.append((random.randint(1,10000),f"Amarnath Reddy {i}",file))
    

# # Prepare a query
query = 'INSERT INTO PROFILE VALUES(%s, %s, %s)'

# # Execute the query and commit the database.
cursor.executemany(query,final_data)
mydb.commit()
