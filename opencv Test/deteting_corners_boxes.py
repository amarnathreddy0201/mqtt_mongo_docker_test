import cv2 as cv
import numpy as np

image = cv.imread("D:\learning\python_learning\opencv Test\OpenCV_Live_Coding\strawberries.jpg",1)

# gray = cv.bitwise_not(image)

# convert to grayscale
gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)

gray = cv.GaussianBlur(gray,(1,1),1)


# threshold
thresh = cv.threshold(gray,150,255,cv.THRESH_TOZERO)[1]


cv.imshow("thresh",thresh)

contours, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)
                                      
# draw contours on the original image
image_copy = image.copy()
#cv.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
for cntr in contours:
    rect = cv.minAreaRect(cntr)
    box = cv.boxPoints(rect)
    box = np.intp(box)
    # draw a green 'nghien' rectangle
    cv.drawContours(image_copy, [box], 0, (0, 255, 0),1)
    


# see the results
cv.imshow(' image_copy', image_copy)
cv.waitKey(0)
# cv.imwrite('contours_none_image1.jpg', image_copy)
cv.destroyAllWindows()



# # get contours
# result = image.copy()
# contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# contours = contours[0] if len(contours) == 2 else contours[1]
# for cntr in contours:
#     x,y,w,h = cv.boundingRect(cntr)
#     cv.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)
#     print("x,y,w,h:",x,y,w,h)
 
# save resulting image
#cv.imwrite('two_blobs_result.jpg',result)      

# show thresh and result    
