# import the opencv library 
import cv2 
import re
import numpy as np
from time import sleep
import subprocess,os
class updatedCamera():
    def __init__(self) -> None:
        self.clickedCoords = []




    def filter(self, low, high, img):
        theMask = cv2.inRange(img, low, high)
        # TODO: Work here
        hsv_color = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        masked = cv2.bitwise_and(hsv_color, img, mask=theMask)
        greyScale = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        blackAndWhite = cv2.threshold(greyScale, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        return blackAndWhite

    def filterImg(self, img):
        img = cv2.resize(img, (640, 640))

        blackAndWhite = self.filter((70, 45, 45), (130, 80, 100), img )
        blackAndWhite2 = self.filter((90, 63, 80), (110, 90, 110), img )
        erodeMask = np.ones((3, 3), np.uint8)
        dilateMask = np.ones((7, 7), np.uint8)

        combined = np.add(blackAndWhite, blackAndWhite2)
        eroded = cv2.erode(combined, erodeMask, iterations=1)
        dilated = cv2.dilate(eroded, dilateMask, iterations=4)


        return dilated

    def splitPic(self, img: np.ndarray):
        color = (0, 0, 255) 
        edited = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        h, w, c = edited.shape
        splitW = int(w/5)
        splitH = int(h/5)
        for i in range(1,6):
            edited = cv2.line(edited, ((i*splitW),0), ((i*splitW), h), color, 9)    

        for i in range(1,6):
            edited = cv2.line(edited, (0,i*splitH), (w, (i*splitH)), color, 9)   
        return self.imageToBitMap(img, splitW, splitH)

    def getWallData(self, img):
        h, w = img.shape
        splitW = int(w/10)
        splitH = int(h/10)
        #RIGHT

        right = img[splitH:9*splitH, splitW*9:w]
        rVal = np.sum(right)/right.size


        left = img[splitH:9*splitH, 0:splitW]
        lVal = np.sum(left)/left.size



        top = img[0:splitH, splitW:splitW*9]
        tVal = np.sum(top)/top.size

        bottom = img[splitH*9:h, splitW:splitW*9]
        bVal = np.sum(bottom)/bottom.size
        return(rVal, lVal, tVal, bVal)

    def click(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            xClick = x
            yClick = y
            clicked = True
            print(xClick)
            print(yClick)
            self.clickedCoords.append((xClick, yClick, clicked))
            print(len(self.clickedCoords))
            return xClick, yClick, clicked



    def ScaledValue(self, img):
        dstCoords = [[0,0], [640, 0], [640,640], [0,640]]
        corners = []
        for vals in self.clickedCoords:
            corners.append([vals[0], vals[1]])
        M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(dstCoords))
        warped = cv2.warpPerspective(img, M, (dstCoords[2][0], dstCoords[2][1]), flags=cv2.INTER_LINEAR)
        return warped

    def transformPhoto(self, img):
        if (len(self.clickedCoords) < 4):
            cv2.imshow('CLICK CORNERS', img)
            (cv2.setMouseCallback('CLICK CORNERS', self.click, img))
            while(len(self.clickedCoords) < 4):

                cv2.waitKey(1) 
            cv2.destroyWindow('CLICK CORNERS')
        dstCoords = [[0,0], [640, 0], [640,640], [0,640]]
        corners = []
        for vals in self.clickedCoords:
            corners.append([vals[0], vals[1]])
        M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(dstCoords))
        warped = cv2.warpPerspective(img, M, (dstCoords[2][0], dstCoords[2][1]), flags=cv2.INTER_LINEAR)
        final = self.filterImg(warped)
        return final





    def imageToBitMap(self, img: np.ndarray, splitW: int, splitH: int):
        bitmap  = np.zeros([9,9], dtype=int)
        for x in range(0, 5):
            for y in range(0, 5):
                lowX = (x*splitW)
                if x == 0:
                    lowX += 1
                highX = (x+1)*splitW
                lowY = (y*splitH)
                if y == 0:
                    lowY +=1
                highY = (y+1)*splitH
                cropped = img[lowY:highY,lowX:highX]
                # cv2.imshow("cropped", cropped)
                rVal, lVal, tVal, bVal = self.getWallData(cropped)
                # cv2.waitKey(0)
                THRESHOLD = 40
                bitmap[2*y, 2*x] = "8"
                if rVal >=  THRESHOLD:
                    if x != 4:
                        bitmap[2*y,2*x+1] = 1
                        if y != 0:
                            bitmap[2*y-1,2*x+1] = 1
             
                        if y != 4:
                            bitmap[2*y+1,2*x+1] = 1
                     
                if bVal >=  THRESHOLD:
                    if y != 4:
                        bitmap[2*y+1,2*x] = 1
             
                        if x!= 0:
                            bitmap[2*y+1,2*x-1] = 1
                        
                        if x!= 4:
                            bitmap[2*y+1,2*x+1] = 1
     
        return bitmap
            

