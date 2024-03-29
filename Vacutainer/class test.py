# Libraries
from pyueye import ueye
import numpy as np
import cv2
import sys
from pyzbar import pyzbar
import csv
import time
import ctypes
import snap7

# ---------------------------------------------------------------------------------------------------------------------------------------

class VacuClass(object):
    def __init__(self):
        # Variables




        # 0: first available camera;  1-254: The camera with the specified camera ID
        self.hCam = ueye.HIDS(0)
        self.sInfo = ueye.SENSORINFO()
        self.cInfo = ueye.CAMINFO()
        self.pcImageMemory = ueye.c_mem_p()
        self.MemID = ueye.int()
        self.rectAOI = ueye.IS_RECT()
        self.pitch = ueye.INT()
        # 24: bits per pixel for color mode; take 8 bits per pixel for monochrome
        self.nBitsPerPixel = ueye.INT(24)
        self.channels = 3  # 3: channels for color mode(RGB); take 1 channel for monochrome
        self.m_nColorMode = ueye.INT(1)		# Y8/RGB16/RGB24/REG32
        self.bytes_per_pixel = int(self.nBitsPerPixel / 8)
        # ---------------------------------------------------------------------------------------------------------------------------------------
        print("START")
        print()



        # Starts the driver and establishes the connection to the camera
        nRet = ueye.is_InitCamera(self.hCam, None)
        if nRet != ueye.IS_SUCCESS:
            print("is_InitCamera ERROR")

        # Reads out the data hard-coded in the non-volatile camera memory and writes it to the data structure that cInfo points to
        nRet = ueye.is_GetCameraInfo(self.hCam, self.cInfo)

        if nRet != ueye.IS_SUCCESS:
            print("is_GetCameraInfo ERROR")

        # You can query additional information about the sensor type used in the camera
        nRet = ueye.is_GetSensorInfo(self.hCam, self.sInfo)
        if nRet != ueye.IS_SUCCESS:
            print("is_GetSensorInfo ERROR")

        nRet = ueye.is_ResetToDefault(self.hCam)
        if nRet != ueye.IS_SUCCESS:
            print("is_ResetToDefault ERROR")

        # Set display mode to DIB
        nRet = ueye.is_SetDisplayMode(self.hCam, ueye.IS_SET_DM_DIB)


        # Set the right color mode
        if int.from_bytes(self.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
            # setup the color depth to the current windows setting
            ueye.is_GetColorDepth(hCam, nBitsPerPixel, m_nColorMode)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_BAYER: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
            print()

        elif int.from_bytes(self.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
            # for color camera models use RGB32 mode
            m_nColorMode = ueye.IS_CM_BGRA8_PACKED
            nBitsPerPixel = ueye.INT(32)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_CBYCRY: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
            print()

        elif int.from_bytes(self.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
            # for color camera models use RGB32 mode
            m_nColorMode = ueye.IS_CM_MONO8
            nBitsPerPixel = ueye.INT(8)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_MONOCHROME: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", bytes_per_pixel)

        else:
            # for monochrome camera models use Y8 mode
            m_nColorMode = ueye.IS_CM_MONO8
            nBitsPerPixel = ueye.INT(8)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("else")


        nSupportedFeatures = ueye.INT()
        nRet = ueye.is_DeviceFeature(self.hCam, ueye.IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_FEATURES,
                                    nSupportedFeatures, ueye.sizeof(nSupportedFeatures))


        #######################################################VERTICAL MERGE MODE CODE###############################################################

        #nVerticalAoiMergeMode = ueye.INT(0)
        #nVerticalAoiMergePosition = ueye.INT(0)


        #nVerticalAoiMergeMode = ueye.INT(ueye.IS_VERTICAL_AOI_MERGE_MODE_FREERUN)
        # nRet = ueye.is_DeviceFeature(hCam, ueye.IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_MODE,
        #                    nVerticalAoiMergeMode, ueye.sizeof(nVerticalAoiMergeMode))

        # if (nRet == ueye.IS_SUCCESS):

        self.pInfo = ueye.SENSORINFO()
        nRet = ueye.is_GetSensorInfo(self.hCam, self.pInfo)


        maxWidth = ueye.INT(self.pInfo.nMaxWidth)
        maxHeight = ueye.INT(self.pInfo.nMaxHeight)


        rectAOI = ueye.IS_RECT()
        rectAOI.s32X = 0
        rectAOI.s32Y = 0
        self.rectAOI.s32Width = 1008
        self.rectAOI.s32Height = 600
        #    nRet = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_SET_AOI, rectAOI, ueye.sizeof(rectAOI))

        #    nVerticalAoiMergePosition = ueye.INT(600)
        #    nRet = ueye.is_DeviceFeature(hCam, ueye.IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_POSITION,
        #                        nVerticalAoiMergePosition, ueye.sizeof(nVerticalAoiMergePosition))

        #######################################################VERTICAL MERGE MODE CODE END###############################################################


        pParam = ueye.wchar_p()
        pParam.value = "testNew.ini"

        ueye.is_ParameterSet(self.hCam, ueye.IS_PARAMETERSET_CMD_LOAD_FILE, pParam, 0)


        # Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
        nRet = ueye.is_AllocImageMem(
            self.hCam, self.rectAOI.s32Width, self.rectAOI.s32Height, self.nBitsPerPixel, self.pcImageMemory, self.MemID)
        if nRet != ueye.IS_SUCCESS:
            print("is_AllocImageMem ERROR")
        else:
            # Makes the specified image memory the active memory
            nRet = ueye.is_SetImageMem(hCam, pcImageMemory, MemID)
            if nRet != ueye.IS_SUCCESS:
                print("is_SetImageMem ERROR")
            else:
                # Set the desired color mode
                nRet = ueye.is_SetColorMode(hCam, m_nColorMode)


        # Activates the camera's live video mode (free run mode)
        nRet = ueye.is_CaptureVideo(self.hCam, ueye.IS_DONT_WAIT)
        if nRet != ueye.IS_SUCCESS:
            print("is_CaptureVideo ERROR")

        # Enables the queue mode for existing image memory sequences
        nRet = ueye.is_InquireImageMem(
            self.hCam, self.pcImageMemory, self.MemID, self.rectAOI.s32Width, self.rectAOI.s32Height, self.nBitsPerPixel, self.pitch)
        if nRet != ueye.IS_SUCCESS:
            print("is_InquireImageMem ERROR")
        else:
            print("Press q to leave the programm")


    def readBarcode(self, frame):
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            # 1
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # 2
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6),
                        font, 2.0, (255, 255, 255), 1)
            # 3
            with open("recognized.txt", mode='a') as file:
                file.write("Recognized Barcode:" + barcode_info)
        return frame


    def findCapColor(self, Image):
        #print("Detecting cap color")

        file = open("recognized.txt", "a")

        CapRectangle = Image[0:599, 0:50]

        average_color_row = np.average(CapRectangle, axis=0)
        average_color = np.average(average_color_row, axis=0)

        Red = average_color[0]
        Green = average_color[1]
        Blue = average_color[2]

        #print(Red, Green, Blue)

        color = ""
        with open('color.csv', 'r+') as fd:
            reader = csv.reader(fd)
            for row in reader:
                difference = (abs(int(row[1])-int(Red)) + abs(
                    int(row[2])-int(Green)) + abs(int(row[3])-int(Blue)))
                if difference < 30:
                    color = row[0]
                    colorName = color
                    break

            if not color:
                print("No accurate match, type new name for this color")
                for line in sys.stdin:
                    for var in line.split():
                        line = line.replace("\n", "")
                        line = line.replace(",", " ")
                        line = line.replace("\"", "")
                        fd.write(f"{line},{int(Red)},{int(Green)},{int(Blue)}\n")
                        colorName = str(line)
                        break
                    break

        #print(difference)

        file.write("Color of cap: ")
        file.write(colorName)
        file.write("\n")

        file.close


    # ---------------------------------------------------------------------------------------------------------------------------------------
    def takeImage(self):
        ueye.is_SetExternalTrigger(self.hCam, ueye.IS_SET_TRIGGER_SOFTWARE)
        bardet = cv2.barcode_BarcodeDetector()


        time.sleep(0.5)



        while(True):

            # Capture a single frame and freeze the video

            time1 = time.time()
            ueye.is_FreezeVideo(self.hCam, ueye.IS_WAIT)

            time2 = time.time()

            print(((time2-time1)-0.161)*1000)

            # Get inage info and process frame for openCV
            array = ueye.get_data(self.pcImageMemory, self.rectAOI.s32Width,
                                self.rectAOI.s32Height, self.nBitsPerPixel, self.pitch, copy=False)
            frame = np.reshape(array, (600, 1008, self.bytes_per_pixel))
            frame = cv2.resize(frame, (0, 0), fx=1, fy=1)

            # Detect barcode of image
            readBarcode(frame)

            # Find cap color of sample in image

            findCapColor(frame)

            # Show image in openCV

            cv2.imshow("Sample Image", frame)

            # Press q if you want to exit loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            return frame    
            time.sleep(1)
    # ---------------------------------------------------------------------------------------------------------------------------------------

    def close(self):

        # Releases an image memory that was allocated using is_AllocImageMem() and removes it from the driver management
        ueye.is_FreeImageMem(hCam, pcImageMemory, MemID)

        # Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
        ueye.is_ExitCamera(hCam)

        # Destroys the OpenCv windows
        cv2.destroyAllWindows()

        print()
        print("END")