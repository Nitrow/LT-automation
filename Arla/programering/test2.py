import numpy as np
import cv2
import time
from imutils.object_detection import non_max_suppression
import pytesseract
from pyzbar.pyzbar import decode
import numpy as np
import time
import colornames

def east_detect(image):
    layerNames = [
    	"feature_fusion/Conv_7/Sigmoid",
    	"feature_fusion/concat_3"]
    
    orig = image.copy()
    orig2 = image.copy()
    
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    (H, W) = image.shape[:2]
    
    # set the new width and height and then determine the ratio in change
    # for both the width and height: Should be multiple of 32
    (newW, newH) = (320, 320)
    
    
    rW = W / float(newW)
    rH = H / float(newH)
    
    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    
    (H, W) = image.shape[:2]
    
    net = cv2.dnn.readNet("/home/asger/Downloads/model/frozen_east_text_detection.pb")
    
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
    	(123.68, 116.78, 103.94), swapRB=True, crop=False)
    
    start = time.time()
    
    net.setInput(blob)
    
    (scores, geometry) = net.forward(layerNames)
    
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
    
        for x in range(0, numCols):
    		# if our score does not have sufficient probability, ignore it
            # Set minimum confidence as required
            if scoresData[x] < 0.1:
                continue
    		# compute the offset factor as our resulting feature maps will
            #  x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
                        
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)
        # draw the bounding box on the image
        cropped = orig2[startY:endY, startX+20:endX+1000
        ]
        cv2.imshow('word', cropped)
        cv2.waitKey()
        text = pytesseract.image_to_string(cropped)
        
        text = text.replace("[", "")
        text = text.replace("", "")


        file.write(text)
        file.write("\n")

        
        

        #print(text)
        #cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)


    
    
    print(time.time() - start)
    return orig

def barcode(image):

    scale_percent = 50 # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)



    barcodes = decode(resized)
    #print(barcodes)
    for barcode in barcodes:

        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
    	    0.5, (0, 0, 255), 2)
        # print the barcode type and data to the terminal
        #print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
    
    #cv2.imshow("Image", image)
    #cv2.waitKey(0)

    if barcodes == []:
        file.write("BARCODE: NONE")
        file.write("\n")
    else:
        file.write("Barcode: ")
        file.write(barcodeData)
        file.write("\n")
   
def color(image):

    height, width = image.shape[:2]

    crop_image = image[int(height*0.5):int(height*0.65), int(width*0.15) :int(width*0.25)]
    avaragePixel = np.average(crop_image, axis = (0,1))

    #print(avaragePixel)

    cv2.imshow("preresult", crop_image)
    # convert to gray
    gray = cv2.cvtColor(crop_image , cv2.COLOR_BGR2GRAY)

    # threshold grayscale image to extract glare
    mask = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)[1]

    result = cv2.inpaint(crop_image, mask, 3, cv2.INPAINT_NS) 

    cv2.imshow("result", result)

    crop_image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    avaragePixel = np.average(crop_image, axis = (0,1))

    #print(avaragePixel)

    colorName = colornames.find(int(avaragePixel[0]), int(avaragePixel[1]),int(avaragePixel[2]))
    
    file.write("Color of cap: ")
    file.write(colorName)
    file.write("\n \n")

    #cv2.imshow("Image", cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB))
    cv2.waitKey(0)  

start = time.time()

file = open("recognized.txt", "a")
#image = cv2.imread("/home/asger/Downloads/sampleText.jpg")
image = cv2.imread("/home/asger/Downloads/sample7.jpg")

color(image)

barcode(image)

out_image = east_detect(image)

cv2.imwrite("/home/asger/Downloads/sample_output.jpg", out_image)

file.write("---------------------------------------------------------------")

end = time.time()
file.close