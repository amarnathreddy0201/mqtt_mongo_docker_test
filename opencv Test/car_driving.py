import cv2
import matplotlib
from matplotlib import colors
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def show(image):
    # Figure size in inches
    plt.figure(figsize=(15, 15))
    
    # Show image, with nearest neighbour interpolation
    plt.imshow(image, interpolation='nearest')
    plt.show()
    
def show_hsv(hsv):
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    show(rgb)
    
def show_mask(mask):
    # plt.figure(figsize=(10, 10))
    # plt.imshow(mask, cmap='gray')
    # plt.show()

    cv2.imshow("image",mask)
    cv2.waitKey(0)
    
def overlay_mask(mask, image):
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
    show(img)




def show_rgb_hist(image):
    colours = ('r','g','b')
    for i, c in enumerate(colours):
        plt.figure(figsize=(20, 4))
        histr = cv2.calcHist([image], [i], None, [256], [0, 256])
#         plt.plot(histr, color=c, lw=2)
        
        if c == 'r': colours = [((i/256, 0, 0)) for i in range(0, 256)]
        if c == 'g': colours = [((0, i/256, 0)) for i in range(0, 256)]
        if c == 'b': colours = [((0, 0, i/256)) for i in range(0, 256)]
        
        plt.bar(range(0, 256), histr, color=colours, edgecolor=colours, width=1)
#         plt.xlim([0, 256])

        plt.show()

def find_biggest_contour(image,main_image):
    
        # Copy to prevent modification
        image = image.copy()
        contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        print (len(contours))

        for cntr in contours:
            area = cv2.contourArea(cntr)
            if(area > 1200):

                rect = cv2.minAreaRect(cntr)
                box = cv2.boxPoints(rect)
                box = np.intp(box)
                # draw a green 'nghien' rectangle
                cv2.drawContours(main_image, [box], 0, (0, 255, 0),5)
        return main_image

if __name__== "__main__":
    try:
        #image = cv2.imread("OpenCV_Live_Coding\strawberries.jpg")

        video = cv2.VideoCapture("OpenCV_Live_Coding\hill-climb.mp4")

        h=0
        w=0        
        if(video.isOpened()):
            suc ,image = video.read()
            h,w,_=image.shape
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter('output.mp4', fourcc, 20.0,(w,h))

        while(video.isOpened()):
            suc ,image = video.read()
            if suc:
                # image = cv2.resize(image,(640,480),cv2.LINE_AA)
                image_blur = cv2.GaussianBlur(image, (5, 5), 0)
                image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
                # 0-10 hue
                min_red = np.array([100, 100, 80])
                max_red = np.array([100, 206, 256])
                image_red1 = cv2.inRange(image_blur_hsv, min_red, max_red)

                # 170-180 hue
                min_red2 = np.array([100, 100, 200])
                max_red2 = np.array([150, 256, 256])
                image_red2 = cv2.inRange(image_blur_hsv, min_red2, max_red2)

                #show_mask(image_red1)
                #show_mask(image_red2)
                image_red = image_red1 + image_red2
                cv2.imshow("image_red",image_red)

                # Clean up
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))

                # image_red_eroded = cv2.morphologyEx(image_red, cv2.MORPH_ERODE, kernel)
                # show_mask(image_red_eroded)

                # image_red_dilated = cv2.morphologyEx(image_red, cv2.MORPH_DILATE, kernel)
                # show_mask(image_red_dilated)

                # image_red_opened = cv2.morphologyEx(image_red, cv2.MORPH_OPEN, kernel)
                # show_mask(image_red_opened)

                # Fill small gaps
                image_red_closed = cv2.morphologyEx(image_red, cv2.MORPH_CLOSE, kernel)
                #show_mask(image_red_closed)

                # Remove specks
                image_red_closed_then_opened = cv2.morphologyEx(image_red_closed, cv2.MORPH_OPEN, kernel)
                # show_mask(image_red_closed_then_opened)

                red_mask = find_biggest_contour(image_red_closed,image)
                out.write(red_mask)
                cv2.imshow("image",image)
                cv2.waitKey(1)
            else:
                break
                
        video.release()
        cv2.destroyAllWindows()
        out.release()
    except Exception as error:
        cv2.destroyAllWindows()
        print(error)

