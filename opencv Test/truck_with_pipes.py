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
        
        i=0

        count_of_tubes =0
        for cntr in contours:
            # if i == 0:
            #     i = 1
            #     continue

            area = cv2.contourArea(cntr)
            
            if(area > 100):
                approx = cv2.approxPolyDP(cntr, 0.01 * cv2.arcLength(cntr, True), True)
                
                
            
                # finding center point of shape
                M = cv2.moments(cntr)
                if M['m00'] != 0.0:
                    x = int(M['m10']/M['m00'])
                    y = int(M['m01']/M['m00'])
            
                # putting shape name at center of each shape
                if len(approx) == 3:
                    continue
                    
            
                elif len(approx) == 4:
                    continue
            
                elif len(approx) == 5:
                    continue
            
                elif len(approx) == 6:
                    continue
            
                else:
                    count_of_tubes+=1
                    # using drawContours() function
                    cv2.drawContours(main_image, [cntr], 0, (0, 255, 0), 1)
                
        return (main_image,count_of_tubes)

if __name__== "__main__":
    image = cv2.imread("truck_with_pipes.jpg",1)
    
    # setting threshold of gray image
    _, threshold = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)

    image_blur_gray = cv2.cvtColor(threshold, cv2.COLOR_RGB2GRAY)

    

    # Clean up
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

    # Fill small gaps
    image_red_closed = cv2.morphologyEx(image_blur_gray, cv2.MORPH_CLOSE, kernel)
    #show_mask(image_red_closed)

    # Remove specks
    image_red_closed_then_opened = cv2.morphologyEx(image_red_closed, cv2.MORPH_OPEN, kernel)
    # show_mask(image_red_closed_then_opened)

    red_mask = find_biggest_contour(image_red_closed,image)

    show_mask(red_mask[0])
    print(red_mask[1])
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        