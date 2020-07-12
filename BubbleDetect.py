# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:19:37 2020

@author: JD
"""
from skimage import measure
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import time
import threading
import copy

from PIL import Image

def bubbleDetect (videoPath,outputPath,minBlobSize,AorBFlag):
    cam = cv2.VideoCapture(videoPath)
    startTime=time.time()
    # frame
    currentFrame = 0
    lineTime=0
    i=0
    backgroundImgHist=np.zeros([180,320,64])

    def calcBackgroundImg(lineList):
        j=0
        for line in range(0,720):
            for col in range(0,1280):
                j+=1
                index=int(lineList[line][col]/4)
                backgroundImg[line][col][index]+=1

    vectFunc=np.vectorize(calcBackgroundImg)

    medianNum=0
    frameList=[]
    while(True):

        # reading from frame
        ret,frame = cam.read()

        if ret:
            frameStartTime=time.time()
            frame=Image.fromarray(frame).convert('L')
            conversionTime=time.time()
            conversionTimeTaken=conversionTime-frameStartTime
            #print("Conversion done: " + str(conversionTimeTaken))
            frame=np.int32(frame)
            floatConversionTime=time.time()
            floatConversionTimeTaken=floatConversionTime-conversionTime
            #print("Float conversion done: :" +str(floatConversionTimeTaken))
            if currentFrame%15==0:
                for line in range(0,len(backgroundImgHist)):
                    for col in range(0,len(backgroundImgHist[line])):
                        backgroundImgHist[line][col][int(frame[line*4][col*4]/4)]+=1
                computeTime=time.time()
                computeTimeTaken=computeTime-floatConversionTime
                #print("Compute done: " + str(computeTimeTaken))
            # increasing counter so that it will
            # show how many frames are created
            currentFrame += 1
        else:
            medianNum=int(currentFrame/30)
            break

    cam.release()
    cv2.destroyAllWindows()

    backgroundImg=np.zeros([720,1280])
    for line in range(0,180):
        for col in range(0,320):
            pixelSum=0
            for bucket in range(0,64):
                pixelSum+=backgroundImgHist[line][col][bucket]
                if pixelSum>=medianNum:
                    for lineOffset in range(0,4):
                        for colOffset in range(0,4):
                            backgroundImg[line*4+lineOffset][col*4+colOffset]=bucket*4
                    break
    plt.imshow(backgroundImg, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()

    def threshold(num):
        if num>30:
            return float(1)
        else:
            return float(0)

    vectorThresh=np.vectorize(threshold)
    regionsList=[]
    bboxListAll=[]
    currentFrame=0
    cam = cv2.VideoCapture(r'C:\Users\JD\Documents\Bubble Research\Videos\2-3-20_vid1\side_trim.mp4')
    while(True):

        # reading from frame
        ret,frame = cam.read()

        if ret:
            frameStartTime=time.time()
            frame=Image.fromarray(frame).convert('L')
            frame=np.int32(frame)
            backgroundImg=np.int32(backgroundImg)
            frame=cv2.absdiff(frame,backgroundImg)
            currentFrame+=1
            frame=vectorThresh(frame)
            start_time=time.time()
            regions=measure.label(frame)
            region_stats=measure.regionprops(regions)
            regionsList=[]
            for region in region_stats:
                if region.bbox_area>minBlobArea and (region.major_axis_length/(region.minor_axis_length+.01))<=2.5 and region.filled_area>12:
                    yWidth=region.bbox[2]-region.bbox[0]
                    xWidth=region.bbox[3]-region.bbox[1]
                    regionsList.append(copy.deepcopy([region.bbox[1]+xWidth/2,region.bbox[0]+yWidth/2,xWidth,yWidth]))
                    cv2.circle(frame,(int(region.bbox[1]+xWidth/2),int(region.bbox[0]+yWidth/2)),10,(255,0,0))
            bboxListAll.append(copy.deepcopy(regionsList))
            regions_time=time.time()
            regions_time_taken=regions_time-start_time
            print(regions_time_taken)
            cv2.imshow('1',frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

    if AorBFlag == "A":
        writeFileName=outputPath+"BubblesA.txt"
    else:
        writeFileName=outputPath+"BubblesB.txt"
    writeFile=open(writeFileName, "w")
    for item in bboxListAll:
        for bubble in item:
            for stat in bubble:
                writeFile.write(str(stat))
                writeFile.write("|")
            writeFile.write("\n")
        writeFile.write("|||\n")
    writeFile.close()

        
