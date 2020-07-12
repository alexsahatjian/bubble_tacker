# -*- coding: utf-8 -*-
"""
This program reads the data from Pathfinder.py and exports data to 2 files Unmatched.txt and DefPath.txt.
Any paths that are not matched are sent to Unmatched.txt and all paths that are matched are sent to DefPath with all x y and z values
"""
import json

def FinalMatch(heightDiff,outputPath,similarFrames):
    '''Read in data from Pathfinder.py'''
    aPaths= outputPath + "A_paths.txt"
    file=open(aPaths)
    data=file.read()
    data=data.replace(", \"end\"",'')
    data=data.split('\n')
    for index in range(0,len(data)):
        data[index]=data[index].split('], [')
        for index1 in range(0,len(data[index])):
            data[index][index1]=data[index][index1].replace("[[",'')
            data[index][index1]=data[index][index1].replace("]]",'')
            data[index][index1]=data[index][index1].split(',')
            for index2 in range(0,len(data[index][index1])):
                try:
                    data[index][index1][index2]=float(data[index][index1][index2])
                except:
                    data.pop(index)
    data.sort(key = lambda data:data[0][4])

    '''Read in data from Pathfinder.py from camera 2'''
    bPaths=outputPath+"B_paths.txt"
    file=open(bPaths)
    dataB=file.read()
    dataB=dataB.replace(", \"end\"",'')
    dataB=dataB.split('\n')
    for index in range(0,len(dataB)):
        dataB[index]=dataB[index].split('], [')
        for index1 in range(0,len(dataB[index])):
            dataB[index][index1]=dataB[index][index1].replace("[[",'')
            dataB[index][index1]=dataB[index][index1].replace("]]",'')
            dataB[index][index1]=dataB[index][index1].split(',')
            for index2 in range(0,len(dataB[index][index1])):
                try:
                    dataB[index][index1][index2]=float(dataB[index][index1][index2])
                except:
                    dataB.pop(index)
    dataB.sort(key = lambda dataB:dataB[0][4])

    defPath={}
    initializedPathsA=[]
    initializedPathsB=[]
    uniquePathCounter=0

    defPathTxt=outputPath+"DefPath.txt"
    writeFile=open(defPathTxt,'w')

    '''for loop to loop over every frame within range 0 to the last frame where a path was tracked'''
    for frameNum in range(0,max(int(data[-1][0][4])+len(data[-1]),int(dataB[-1][0][4])+len(dataB[-1]))):
        i=0
        j=0
        maxHeightDiff=heightDiff
        '''This while loop checks to see if the first index in data has starting frame num equal to the frame num given by for loop
        While i increases if a path matches so that more than 1 path can be seen as initialized per frame'''
        while i>=0:
            if len(data)==i:
                break
            '''While looping through frames find paths that start at the given frame (ie find when paths are initialized)'''
            matchNum=0
            if data[i][0][4]==frameNum:
                pathFound=False
                newPathFound=False
                '''This part still needs to be done and matches paths to defPaths that have lost data from one camera but the path from the other camera is still going'''
                for pathNum, path in defPath.items():
                    #TODO match vs defPath
                    '''matchNum is a dummy variable used to flag matches and nonmatches at different places throughout the program'''
                    pathMatchBool=False
                    lengthFlag=False
                    initPathIndex=int(frameNum-path[0][5])
                    if "|" in str(path[initPathIndex][0]):
                        pathMatchBool=True
                        for frame in range(0,min(len(data[i]),len(path)-initPathIndex)):
                            '''add length flag so there must be atleast 3 frames matched to eachother to consider a match'''
                            if frame==similarFrames:
                                lengthFlag=True
                            if abs(path[initPathIndex+frame][2]-data[i][frame][1])>=maxHeightDiff:
                                pathMatchBool=False
                                break
                        if pathMatchBool==True and lengthFlag==True:
                            pathFound=True
                            for pos in range(0,max(len(data[i]),len(path)-initPathIndex)):
                                try:
                                    path[initPathIndex+pos][0]=data[i][pos][0]
                                except:
                                    try:
                                        path.append([data[i][pos][0],"|"+str(path[-1][1]),data[i][pos][1],data[i][pos][2],data[i][pos][3]])
                                    except:
                                        path[initPathIndex+pos][0]="|"+str(data[i][-1][0])
                            break
                '''If a match was not found against defPaths'''
                if(pathFound==False):
                    '''for all unmatched paths in other frame'''
                    for pathNum in range(0,len(initializedPathsB)):
                        pathMatchBool=True
                        lengthFlag=False
                        '''Find the index of the unmatched path that corresponds to the current frame'''
                        initPathIndex=int(frameNum-initializedPathsB[pathNum][0][4])
                        '''Loop over all heights to see if they match all the way to end of whichever path ends first'''
                        for timeNum in range(0, min(len(data[i]),len(initializedPathsB[pathNum])-initPathIndex)):
                            if timeNum==similarFrames:
                                lengthFlag=True
                            if abs(data[i][timeNum][1]-initializedPathsB[pathNum][timeNum+initPathIndex][1])>=maxHeightDiff:
                                pathMatchBool=False
                                break
                        '''If a match is confirmed create a new path that now has x y and z positions and add it to a dictionary where they key is a running counter of unique paths
                        This path will use the last/first tracked position of a path that does not entirely overlap with the other path
                        (ie Imagine the first camera tracks for 5 more frames. The last known position of the other camera will be used for those 5 frames that do not overlap)'''
                        if pathMatchBool==True:
                            #TODO
                            addPath=[]
                            for pos in range(0,initPathIndex):
                                addPath.append([data[i][0][0],initializedPathsB[pathNum][pos][0],initializedPathsB[pathNum][pos][1],initializedPathsB[pathNum][pos][2],initializedPathsB[pathNum][pos][3]])
                            for pos in range(0,max(len(data[i]),len(initializedPathsB[pathNum])-initPathIndex)):
                                try:
                                    addPath.append([data[i][pos][0],initializedPathsB[pathNum][pos+initPathIndex][0],data[i][pos][1],data[i][pos][2],data[i][pos][3]])
                                except:
                                    try:
                                        addPath.append([data[i][pos][0],"|"+str(initializedPathsB[pathNum][-1][0]),data[i][pos][1],data[i][pos][2],data[i][pos][3]])
                                    except:
                                        addPath.append(["|"+str(data[i][-1][0]),initializedPathsB[pathNum][pos+initPathIndex][0],initializedPathsB[pathNum][pos+initPathIndex][1],initializedPathsB[pathNum][pos+initPathIndex][2],initializedPathsB[pathNum][pos+initPathIndex][3]])
                            addPath[0].append(initializedPathsB[pathNum][0][-1])
                            defPath[uniquePathCounter]=addPath
                            newPathFound=True
                            uniquePathCounter+=1
                            break
                    '''If a match is found remove the unmatched path from the unmatched path list'''
                    '''Else add this path to the list of unmatched paths from its own camera'''
                if newPathFound==True:
                    initializedPathsB.pop(matchNum)
                elif pathFound==False and newPathFound==False:
                    initializedPathsA.append(data[i])
                i+=1
                '''remove the path from the intial data list'''
            else:
                for index in range(0,i):
                    data.pop(0)
                i=-1





        '''------------Part B----------------'''
        '''This while loop checks to see if the first index in data has starting frame num equal to the frame num given by for loop
        While i increases if a path matches so that more than 1 path can be seen as initialized per frame'''
        while j>=0:
            '''While looping through frames find paths that start at the given frame (ie find when paths are initialized)'''
            matchNum=0
            if len(dataB)==j:
                break
            if dataB[j][0][4]==frameNum:
                pathFound=False
                newPathFound=False
                '''This part still needs to be done and matches paths to defPaths that have lost data from one camera but the path from the other camera is still going'''
                for pathNum,path in defPath.items():
                    #TODO match vs defPath
                    '''matchNum is a dummy variable used to flag matches and nonmatches at different places throughout the program'''
                    pathMatchBool=False
                    lengthFlag=False
                    initPathIndex=int(frameNum-path[0][5])
                    if "|" in str(path[initPathIndex][1]):
                        pathMatchBool=True
                        for frame in range(0,min(len(dataB[j]),len(path)-initPathIndex)):
                            '''add length flag so there must be atleast 3 frames matched to eachother to consider a match'''
                            if frame==similarFrames:
                                lengthFlag=True
                            if abs(path[initPathIndex+frame][2]-dataB[j][frame][1])>=maxHeightDiff:
                                pathMatchBool=False
                                break
                        if pathMatchBool==True and lengthFlag==True:
                            pathFound=True
                            for pos in range(0,max(len(dataB[j]),len(path)-initPathIndex)):
                                try:
                                    path[initPathIndex+pos][1]=dataB[j][pos][0]
                                except:
                                    try:
                                        path.append(["|"+str(path[-1][0]),dataB[j][pos][0],dataB[j][pos][1],dataB[j][pos][2],dataB[j][pos][3]])
                                    except:
                                        path[initPathIndex+pos][1]="|"+str(dataB[j][-1][0])
                '''If a match was not found against defPaths'''
                if(pathFound==False):
                    '''for all unmatched paths in other frame'''
                    for pathNum in range(0,len(initializedPathsA)):
                        pathMatchBool=True
                        lengthFlag=False
                        '''Find the index of the unmatched path that corresponds to the current frame'''
                        initPathIndex=int(frameNum-initializedPathsA[pathNum][0][4])
                        '''Loop over all heights to see if they match all the way to end of whichever path ends first'''
                        for timeNum in range(0, min(len(dataB[j]),len(initializedPathsA[pathNum])-initPathIndex)):
                            if timeNum==similarFrames:
                                lengthFlag=True
                            if abs(dataB[j][timeNum][1]-initializedPathsA[pathNum][timeNum+initPathIndex][1])>=maxHeightDiff:
                                pathMatchBool=False
                                break
                        '''If a match is confirmed create a new path that now has x y and z positions and add it to a dictionary where they key is a running counter of unique paths
                        This path will use the last/first tracked position of a path that does not entirely overlap with the other path
                        (ie Imagine the first camera tracks for 5 more frames. The last known position of the other camera will be used for those 5 frames that do not overlap)'''
                        if pathMatchBool==True and lengthFlag==True:
                            #TODO
                            addPath=[]
                            for pos in range(0,initPathIndex):
                                addPath.append([initializedPathsA[pathNum][pos][0],dataB[j][0][0],initializedPathsA[pathNum][pos][1],initializedPathsA[pathNum][pos][2],initializedPathsA[pathNum][pos][3]])
                            for pos in range(0,max(len(dataB[j]),len(initializedPathsA[pathNum])-initPathIndex)):
                                try:
                                    addPath.append([initializedPathsA[pathNum][pos+initPathIndex][0],dataB[j][pos][0],dataB[j][pos][1],dataB[j][pos][2],dataB[j][pos][3]])
                                except:
                                    try:
                                        addPath.append(["|"+str(initializedPathsA[pathNum][-1][0]),dataB[j][pos][0],dataB[j][pos][1],dataB[j][pos][2],dataB[j][pos][3]])
                                    except:
                                        addPath.append([initializedPathsA[pathNum][pos+initPathIndex][0],"|"+str(dataB[j][-1][0]),initializedPathsA[pathNum][pos+initPathIndex][1],initializedPathsA[pathNum][pos+initPathIndex][2],initializedPathsA[pathNum][pos+initPathIndex][3]])
                            addPath[0].append(initializedPathsA[pathNum][0][-1])
                            defPath[uniquePathCounter]=addPath
                            newPathFound=True
                            uniquePathCounter+=1
                            break
                    '''If a match is found remove the unmatched path from the unmatched path list'''
                    '''Else add this path to the list of unmatched paths from its own camera'''
                if newPathFound==True:
                    initializedPathsA.pop(matchNum)
                elif newPathFound==False and pathFound==False:
                    initializedPathsB.append(dataB[j])
                j+=1
                '''remove the path from the intial data list'''
            else:
                for index in range(0,j):
                    dataB.pop(0)
                j=-1


        '''This block removes any unmatched paths from the unmatched list if their final frame has been passed
        (ie cant be matched) and writes it to the Unmatched.txt file'''
        removeList=[]
        unmatchedTxtA=outputPath+"UnmatchedA.txt"
        writeUnmatched=open(unmatchedTxtA,'w')
        for path in range(0,len(initializedPathsA)):
            lastFrame=len(initializedPathsA[path])+initializedPathsA[path][0][4]-1
            if frameNum>=lastFrame:
                json.dump(initializedPathsA[path],writeUnmatched)
                writeUnmatched.write("\n")
                removeList.append(initializedPathsA[path])
        if len(removeList)>=1:
            initializedPathsA=[path for path in initializedPathsA if path not in removeList]

        removeList=[]
        unmatchedTxtB=outputPath+"UnmatchedB.txt"
        writeUnmatched2=open(unmatchedTxtB,'w')
        for path in range(0,len(initializedPathsB)):
            lastFrame=len(initializedPathsB[path])+initializedPathsB[path][0][4]-1
            if frameNum>=lastFrame:
                json.dump(initializedPathsB[path],writeUnmatched2)
                writeUnmatched2.write("\n")
                removeList.append(initializedPathsB[path])
        if len(removeList)>=1:
            initializedPathsB=[path for path in initializedPathsB if path not in removeList]

        '''This block removes any defined paths whose last tracked frame has been passed and writes their data to DefPath.txt'''
        removeList=[]
        for key,path in defPath.items():
            lastFrame=len(path)+path[0][5]-1
            if frameNum>=lastFrame:
                json.dump((key, path),writeFile)
                writeFile.write('\n')
                removeList.append(path)
        defPath = {key:val for key, val in defPath.items() if val not in removeList}


    writeFile.close()

