
import numpy as np
import cv2

img = cv2.imread('/home/asger/Pictures/greenbox2.jpg')

scale_percent = 30 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

resized = ~resized

imgGry = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#print(contours , hierarchy )

for i in range(len(contours)):
    print(cv2.contourArea(contours[i]))


for i in range(len(contours)):
    if cv2.contourArea(contours[i]) > 1000 and cv2.contourArea(contours[i]) < 10000000 :
    
            approx = cv2.approxPolyDP(contours[i], 0.05, True)

    
            cv2.drawContours(resized, [approx], 0, (0, 0, 0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5
            if len(approx) == 4 :
                x, y , w, h = cv2.boundingRect(approx)
                aspectRatio = float(w)/h
                #print(aspectRatio)




            cv2.putText(resized, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))


cv2.imshow('shapes', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()


import cv2
import numpy as np
from matplotlib import pyplot as plt

# reading image
img = cv2.imread('/home/asger/Pictures/greenbox2.jpg')

resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

resized = ~resized

# converting image into grayscale image
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# setting threshold of gray image
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# using a findContours() function
contours, _ = cv2.findContours(
	threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

i = 0

# list for storing names of shapes
for i in range(len(contours)):
    if cv2.contourArea(contours[i]) > 1300 and cv2.contourArea(contours[i]) < 1500 :

	    # here we are ignoring first counter because
	    # findcontour function detects whole image as shape
	    if i == 0:
		    i = 1
		    continue

	# cv2.approxPloyDP() function to approximate the shape
	    approx = cv2.approxPolyDP(
		    contours[i], 0.01, True)
	
	# using drawContours() function
	    cv2.drawContours(resized, [contours[i]], 0, (0, 0, 0), 5)

	# finding center point of shape
	    M = cv2.moments(contours[i])
	    if M['m00'] != 0.0:
		    x = int(M['m10']/M['m00'])
		    y = int(M['m01']/M['m00'])

	# putting shape name at center of each shape
	    if len(approx) == 3:
		    cv2.putText(resized, 'Triangle', (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

	    elif len(approx) == 4:
		    cv2.putText(resized, 'Quadrilateral', (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

	    elif len(approx) == 5:
		    cv2.putText(resized, 'Pentagon', (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

	    elif len(approx) == 6:
		    cv2.putText(resized, 'Hexagon', (x, y),
			    		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

	    else:
		    cv2.putText(resized, 'circle', (x, y),
			    		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)


print(x, y)
# displaying the image after drawing contours
cv2.imshow('shapes', resized)

cv2.waitKey(0)
cv2.destroyAllWindows()



