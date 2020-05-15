'''
This program takes the data file from the BubbleTracker.m file and creates a list of paths
A path is defined as a list of positions and size measurements of a bubble at each frame
This will export all data to a file named A_paths.txt
'''

'''import necessary libraries'''
import json
import copy
import numpy as np
'''
This function matches all bubbles in one frame to a list of paths (ie finds continuation of paths)
toMatch is the list of paths to match while unmatched is the list of bubbles in the next frame
This function automatically adds the bubble to the path if matched
A bubble is considered a match if it is the only bubble with in a 40 pixle radius of the last recorded position in a path
A "complication occurs if there is more than one bubble in the 40 pixle radius and a list of complications is returned 
A complications is a list as follows [[possibleMatch][possibleMatch][possibleMatch]....[pathToMatchTo]]
'''
maxDiff=.3
def findPathMatches(unmatched,toMatch):
    complicationsList=[]
    removeList=[]
    for index in range(0,len(toMatch)):
        possibleMatch=[]
        complications=[]
        for index1 in range(0,len(unmatched)):
            xdiff=toMatch[index][-1][0]-unmatched[index1][0]
            ydiff=toMatch[index][-1][1]-unmatched[index1][1]
            totalDiff=ydiff**2+xdiff**2
            if(totalDiff**.5<maxDiff):
                possibleMatch.append(copy.deepcopy(unmatched[index1]))
        if(len(possibleMatch)==1):
            toMatch[index].append(possibleMatch[0])
            unmatched[:]=[bubble for bubble in unmatched if bubble not in possibleMatch]
        elif(len(possibleMatch)==0):
            toMatch[index].append("end")
        else:
            complications.append(possibleMatch)
            complications.append(toMatch[index])
            complicationsList.append(complications)
            removeList.append(toMatch[index])
    toMatch[:]=[path for path in toMatch if path not in removeList]
    if complicationsList!=[]: 
        return complicationsList

'''
This function works the same as the previous function but is used to find the first match of a path
If a match is found it appends the match to the given 'sendList' and attaches the starting frame to the first position list
A new path looks as follows: [[x1,z1,height,width,startingFrame][x2,z2,height2,width2]]
Like in the previous function a list of complictaions is returned 
'''
def findPrelimMatches(prevFrame,currFrame,sendList,frameNum):
    complicationsList=[]
    bubbleMatch=[]
    for index in range(0,len(prevFrame)):
        possibleMatch=[]
        for index1 in range(0,len(currFrame)):
            xdiff=prevFrame[index][0]-currFrame[index1][0]
            ydiff=prevFrame[index][1]-currFrame[index1][1]
            totalDiff=(ydiff**2+xdiff**2)**.5
            if(totalDiff<maxDiff):
                if len(possibleMatch)==0:
                    possibleMatch.append(copy.deepcopy(prevFrame[index]))
                possibleMatch.append(currFrame[index1])
        for index in range(0,len(possibleMatch)):   
            bubbleMatch.append(copy.deepcopy(possibleMatch[index]))
        if(len(possibleMatch)==2):
            for index in range(0,len(possibleMatch)):   
                bubbleMatch.append(copy.deepcopy(possibleMatch[index]))
            possibleMatch[0].append(frameNum)
            sendList.append(possibleMatch)
        elif len(possibleMatch)>=3:
            possibleMatch[0].append(frameNum)
            complicationsList.append(possibleMatch)
    currFrame[:]=[path for path in currFrame if path not in bubbleMatch]
    prevFrame[:]=[path for path in prevFrame if path not in bubbleMatch]
    return complicationsList

'''
This function handles the complication list from the findPrelimMatches function by selecting the bubble that is closest 
to the bubble in the previous frame. This function returns a lists of new paths. 
'''
def complicationHandleDist(complicationsList):
    returnList=[]
    for complication in complicationsList:
        leastDist=5000
        pathList=['dummy']
        for item in range(1,len(complication)):
            dist=(complication[0][0]-complication[item][0])**2+(complication[0][1]-complication[item][1])**2
            if dist<leastDist:
                leastDist=dist
                pathList=[]
                pathList.append(complication[item])
        listReturn=[complication[0],pathList[0]]
        returnList.append(listReturn)
    if len(returnList)>=1:
        return returnList

'''
This function handles complications from the findPathMatches function by calculating the average velocity and acceleration
of the path and selects the bubble closest to the predicted position and returns the path with the newly added position
'''
def complicationHandleVelocity(complicationsList):
    returnList=[]
    if complicationsList==None:
        return
    for complication in complicationsList:
        leastDist=5000
        expectedPos=[0,0]
        pathList=['dubby']
        if len(complication[-1])==2:
            xvel=complication[-1][-1][0]-complication[-1][-2][0]
            yvel=complication[-1][-1][1]-complication[-1][-2][1]
            expectedPos[0]=complication[-1][-1][0]+xvel
            expectedPos[1]=complication[-1][-1][1]+yvel
        else:
            xvel=complication[-1][-1][0]-complication[-1][-2][0]
            yvel=complication[-1][-1][1]-complication[-1][-2][1]
            xvel2=complication[-1][-2][0]-complication[-1][-3][0]
            yvel2=complication[-1][-2][1]-complication[-1][-3][1]
            accX=xvel2-xvel
            accY=yvel2-yvel
            xchange=xvel+accX
            ychange=yvel+accY
            expectedPos[0]=complication[-1][-1][0]+xchange
            expectedPos[1]=complication[-1][-1][1]+ychange
        for item in range(0,len(complication[0])):
            dist=(expectedPos[0]-complication[0][item][0])**2+(expectedPos[1]-complication[0][item][1])**2
            if dist<leastDist:
                leastDist=dist
                pathList=[]
                pathList.append(complication[0][item])
        complication[-1].append(pathList[0])
        returnList.append(complication[-1])
    if len(returnList)>=1:
        return returnList

def priorityCompicationHandle(currentTrackList,nextFrame):
    while len(currentTrackList)!=0:
        overlapTracks=[]
        overlapArea=[]
        matchFoundBool=False
        for track in range(1,len(currentTrackList)):
            if abs(currentTrackList[0][-1][0]-currentTrackList[track][-1][0])<2*maxDiff and abs(currentTrackList[0][-1][1]-currentTrackList[track][-1][1])<2*maxDiff:
                overlapTracks.append(currentTrackList[track])
        for track in overlapTracks:
            xVal=(track[-1][0]+currentTrackList[0][-1][0])/2
            yVal=(track[-1][1]+currentTrackList[0][-1][1])/2
            xDist=(2*maxDiff-abs(track[-1][0]-currentTrackList[0][-1][0]))/2
            yDist=(2*maxDiff-abs(track[-1][1]-currentTrackList[0][-1][1]))/2
            overlapArea.append([xVal,yVal,xDist,yDist])
        for bubble in nextFrame:
            areaIndecies=[]
            distList=[]
            for area in range(0,len(overlapArea)):
                if bubble[0]>overlapArea[area][0]-overlapArea[area][2] and bubble[0]<overlapArea[area][0]+overlapArea[area][2] and bubble[1]>overlapArea[area][1]-overlapArea[area][3] and bubble[1]<overlapArea[area][1]+overlapArea[area][3]:
                    areaIndecies.append(area)
            if areaIndecies !=[]:
                for index in areaIndecies:
                    try:
                        xVel1=overlapTracks[index][-1][0]-overlapTracks[index][-2][0]
                        yVel1=overlapTracks[index][-1][1]-overlapTracks[index][-2][1]
                        xVel2=overlapTracks[index][-2][0]-overlapTracks[index][-3][0]
                        yVel2=overlapTracks[index][-2][1]-overlapTracks[index][-3][1]
                        xAccel=xVel1-xVel2
                        yAccel=yVel1-yVel2
                        xVel=xVel1+xAccel
                        yVel=yVel1+yAccel
                    except:
                        xVel=overlapTracks[index][-1][0]-overlapTracks[index][-2][0]
                        yVel=overlapTracks[index][-1][1]-overlapTracks[index][-2][1]
                    posXPredict=overlapTracks[index][-1][0]+xVel
                    posYPredict=overlapTracks[index][-1][1]+yVel
                    dist=((posXPredict-overlapTracks[index][-1][0])**2+(posYPredict-overlapTracks[index][-1][0])**2)**.5
                    distList.append([dist,index])
                distList.sort(key=lambda x: x[0])
                overlapTracks[distList[0][1]].append(bubble)
                currentTrackList.remove(overlapTracks[distList[0][1]])
                nextFrame.remove(bubble)
                matchFoundBool=True
                break
        if matchFoundBool==False:
            currentTrackList.pop(0)
                
'''Read data from BubbleTracker.m'''
file=open('A.txt')
data=file.read()
data=data.split('|||\n')
for frame in range(0,len(data)):
    data[frame]=data[frame].split('\n')
    for path in range(0,len(data[frame])):
        data[frame][path]=data[frame][path].split('|')
        for element in range(0,len(data[frame][path])):
            try:
                data[frame][path][element]=float(data[frame][path][element])
            #remove empty elements ie []
            except:
                data[frame][path].remove(data[frame][path][element])                
#data.pop(0)

'''Add heights and widths to position becuase positions given are from the top left corner and we want centroid data'''
for frame in range(0,len(data)):
    data[frame] = [x for x in data[frame] if x != []]
#    for path in range(0,len(data[frame])):
#        data[frame][path][0]=data[frame][path][0]+(data[frame][path][2]/2)
#        data[frame][path][1]=data[frame][path][1]+(data[frame][path][3]/2)
        
'''scale video pixles to cm and correct axis'''
originX,originY=278,100
pixleToCM=140
angleX=(.635/360)*np.pi*2  

for frame in range(0,len(data)):
    removeList=[]
    for bubble in data[frame]:
        bubble[0]=(bubble[0]-originX)/pixleToCM
        bubble[1]=(bubble[1]-originY)/pixleToCM
        bubble[0]=bubble[0]*np.cos(angleX)-bubble[1]*np.sin(angleX)
        bubble[1]=bubble[0]*np.sin(angleX)+bubble[1]*np.cos(angleX)
        bubble[2]=bubble[2]/pixleToCM
        bubble[3]=bubble[3]/pixleToCM
        if bubble[1]<=(originY/pixleToCM)+.1:
            removeList.append(bubble)
    data[frame]=[bubble for bubble in data[frame] if bubble not in removeList]

'''Read data from BubbleTracker.m'''
file=open('B.txt')
dataB=file.read()
dataB=dataB.split('|||\n')
for frame in range(0,len(dataB)):
    dataB[frame]=dataB[frame].split('\n')
    for path in range(0,len(dataB[frame])):
        dataB[frame][path]=dataB[frame][path].split('|')
        for element in range(0,len(dataB[frame][path])):
            try:
                dataB[frame][path][element]=float(dataB[frame][path][element])
            #remove empty elements ie []
            except:
                dataB[frame][path].remove(dataB[frame][path][element])                
#dataB.pop(0)

'''Add heights and widths to position becuase positions given are from the top left corner and we want centroid data'''
for frame in range(0,len(dataB)):
    dataB[frame] = [x for x in dataB[frame] if x != []]
#    for path in range(0,len(dataB[frame])):
#        dataB[frame][path][0]=dataB[frame][path][0]+(dataB[frame][path][2]/2)
#        dataB[frame][path][1]=dataB[frame][path][1]+(dataB[frame][path][3]/2)
        
BoriginX,BoriginY=168,37
BpixleToCM=170.6
BangleX=(-1.7/360)*np.pi*2  


for frame in range(0,len(dataB)):
    removeList=[]
    for bubble in dataB[frame]:
        bubble[0]=(bubble[0]-BoriginX)/BpixleToCM
        bubble[1]=(bubble[1]-BoriginY)/BpixleToCM
        bubble[0]=bubble[0]*np.cos(BangleX)-bubble[1]*np.sin(BangleX)
        bubble[1]=bubble[0]*np.sin(BangleX)+bubble[1]*np.cos(BangleX)
        bubble[2]=bubble[2]/BpixleToCM
        bubble[3]=bubble[3]/BpixleToCM
        if bubble[1]<=(BoriginY/BpixleToCM)+.1:
            removeList.append(bubble)
    dataB[frame]=[bubble for bubble in dataB[frame] if bubble not in removeList]
    

'''Open write file. Change this line if you want to change the name of the outputfile'''
writeFile=open("A_paths.txt","w")
writeFile2=open("B_paths.txt","w")


map(float,data)
map(float,dataB)
firstMatch=[]
secondMatch=[]
thirdMatch=[]
firstMatchB=[]
secondMatchB=[]
thirdMatchB=[]
defPathA=[]
defPathB=[]

'''
removeList is used alot in order export positions that need to be removed from the data out of for loops.
If I were to try to remove indecies within the for loops the for loop will eventually return "index does not exist"
error becuase all for loops are determined from lenegth of a list and when the list is made smaller the for loop 
still iterates over the inital size of the list
'''
removeList=[]

'''create a for loop that cycles over every frame from the video'''
for frame in range(1,min((len(data)-1),(len(dataB)-1))):
    currentTrackListA=[]
    currentTrackListB=[]
    currentTrackListA.extend(defPathA)
    currentTrackListA.extend(thirdMatch)
    currentTrackListA.extend(secondMatch)
    currentTrackListA.extend(firstMatch)
    currentTrackListB.extend(defPathB)
    currentTrackListB.extend(thirdMatchB)
    currentTrackListB.extend(secondMatchB)
    currentTrackListB.extend(firstMatchB)
    priorityCompicationHandle(currentTrackListA,data[frame])
    priorityCompicationHandle(currentTrackListB,dataB[frame])
    
    
    '''
    Here all paths are being compared to the frame to find continuations of the path.
    I have required that all paths must have length 5 to be considered a defined path in order to filter out any 
    paths that would not be useful to analyze
    Notice how remove list is cleared and used to remove positions from the list 'data'
    '''
    removeList=[]
    complication=findPathMatches(data[frame],defPathA)
    pathlist=complicationHandleVelocity(complication)
    if pathlist:
        for item in range(0,len(pathlist)):
            defPathA.append(pathlist[item])
            removeList.append(pathlist[item][-1])
    data[frame]=[bubble for bubble in data[frame] if bubble not in removeList]
    
    removeList=[]
    complication=findPathMatches(data[frame],thirdMatch)
    pathlist=complicationHandleVelocity(complication)
    if pathlist:
        for item in range(0,len(pathlist)):
            thirdMatch.append(pathlist[item])
            removeList.append(pathlist[item][-1])
    data[frame]=[bubble for bubble in data[frame] if bubble not in removeList]
    
    removeList=[]
    complication=findPathMatches(data[frame],secondMatch)
    pathlist=complicationHandleVelocity(complication)
    if pathlist:
        for item in range(0,len(pathlist)):
            secondMatch.append(pathlist[item])
            removeList.append(pathlist[item][-1])
    data[frame]=[bubble for bubble in data[frame] if bubble not in removeList]
    
    removeList=[]
    complication=findPathMatches(data[frame],firstMatch)
    pathlist=complicationHandleVelocity(complication)
    if pathlist:
        for item in range(0,len(pathlist)):
            firstMatch.append(pathlist[item])
            removeList.append(pathlist[item][-1])
    data[frame]=[bubble for bubble in data[frame] if bubble not in removeList]
    
    removeList=[]
    complication=findPathMatches(dataB[frame],defPathB)
    pathlist=complicationHandleVelocity(complication)
    if pathlist:
        for item in range(0,len(pathlist)):
            defPathB.append(pathlist[item])
            removeList.append(pathlist[item][-1])
    dataB[frame]=[bubble for bubble in dataB[frame] if bubble not in removeList]
    
    removeList=[]
    complication=findPathMatches(dataB[frame],thirdMatchB)
    pathlist=complicationHandleVelocity(complication)
    if pathlist:
        for item in range(0,len(pathlist)):
            thirdMatchB.append(pathlist[item])
            removeList.append(pathlist[item][-1])
    dataB[frame]=[bubble for bubble in dataB[frame] if bubble not in removeList]
    
    removeList=[]
    complication=findPathMatches(dataB[frame],secondMatchB)
    pathlist=complicationHandleVelocity(complication)
    if pathlist:
        for item in range(0,len(pathlist)):
            secondMatchB.append(pathlist[item])
            removeList.append(pathlist[item][-1])
    dataB[frame]=[bubble for bubble in dataB[frame] if bubble not in removeList]
    
    removeList=[]
    complication=findPathMatches(dataB[frame],firstMatchB)
    pathlist=complicationHandleVelocity(complication)
    if pathlist:
        for item in range(0,len(pathlist)):
            firstMatchB.append(pathlist[item])
            removeList.append(pathlist[item][-1])
    dataB[frame]=[bubble for bubble in dataB[frame] if bubble not in removeList]
    
    
    '''These two blocks find the prelim matches'''
    removeList=[]
    complication=findPrelimMatches(data[frame-1],data[frame],firstMatch,frame-1)
    pathlist=complicationHandleDist(complication)
    if pathlist:
        for item in range(0,len(pathlist)):
            firstMatch.append(copy.deepcopy(pathlist[item]))
            for index in range(0,1):
                removeList.append(pathlist[item][index])
    data[frame]=[bubble for bubble in data[frame] if bubble not in removeList]
    data[frame-1]=[bubble for bubble in data[frame-1] if bubble not in removeList]
    
    removeList=[]
    complication=findPrelimMatches(dataB[frame-1],dataB[frame],firstMatchB,frame-1)
    pathlist=complicationHandleDist(complication)
    if pathlist:
        for item in range(0,len(pathlist)):
            firstMatchB.append(copy.deepcopy(pathlist[item]))
            for index in range(0,1):
                removeList.append(pathlist[item][index])
    data[frame]=[bubble for bubble in data[frame] if bubble not in removeList]
    data[frame-1]=[bubble for bubble in data[frame-1] if bubble not in removeList]
    
    '''
    This block of code sorts through all the list moving any list that was coninued in the frame to the next level 
    (ie from secondMatch to thirdMatch) and also removes any paths from those list that were not continued
    '''
    removeList=[]
    for item in firstMatch:
        if item[-1]=="end":
            removeList.append(item)
        elif len(item)==3:
            secondMatch.append(item)
            removeList.append(item)
    if len(removeList)>=1:
        firstMatch=[path for path in firstMatch if path not in removeList]
    removeList=[]
    for item in secondMatch:
        if item[-1]=="end":
            removeList.append(item)
        elif len(item)==4:
            thirdMatch.append(item)
            removeList.append(item)
    if len(removeList)>=1:
        secondMatch=[path for path in secondMatch if path not in removeList]
    removeList=[]
    for item in thirdMatch:
        if item[-1]=="end":
            removeList.append(item)
        elif len(item)==5:
            defPathA.append(item)
            removeList.append(item)
    if len(removeList)>=1:
        thirdMatch=[path for path in thirdMatch if path not in removeList]
    removeList=[]
    for item in firstMatchB:
        if item[-1]=="end":
            removeList.append(item)
        elif len(item)==3:
            secondMatchB.append(item)
            removeList.append(item)
    if len(removeList)>=1:
        firstMatchB=[path for path in firstMatchB if path not in removeList]
    removeList=[]
    for item in secondMatchB:
        if item[-1]=="end":
            removeList.append(item)
        elif len(item)==4:
            thirdMatchB.append(item)
            removeList.append(item)
    if len(removeList)>=1:
        secondMatchB=[path for path in secondMatchB if path not in removeList]
    removeList=[]
    for item in thirdMatchB:
        if item[-1]=="end":
            removeList.append(item)
        elif len(item)==5:
            defPathB.append(item)
            removeList.append(item)
    if len(removeList)>=1:
        thirdMatchB=[path for path in thirdMatchB if path not in removeList]
    
    '''When a "defeined path" is not continued to the next frame it is removed from the list and written to the output file'''
    removeList=[]
    for item in defPathA:
        if item[-1]=="end":
            json.dump(item,writeFile)
            writeFile.write("\n")
            removeList.append(item)
    if len(removeList)>=1:
        defPathA=[path for path in defPathA if path not in removeList]
    removeList=[]
    for item in defPathB:
        if item[-1]=="end":
            json.dump(item,writeFile2)
            writeFile2.write("\n")
            removeList.append(item)
    if len(removeList)>=1:
        defPathB=[path for path in defPathB if path not in removeList]
        
for item in defPathA:
    json.dump(item,writeFile)
    writeFile.write("\n")
for item in defPathB:
    json.dump(item,writeFile2)
    writeFile2.write("\n")
'''close file write file to ensure all paths are written'''        
writeFile.close()
writeFile2.close()
    
            

    
