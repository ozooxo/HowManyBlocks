from __future__ import division
from __future__ import print_function

import shelve
import math
import time

from configuration import *

import pyglet
from pyglet.gl import *

class OneTaskScore:
    def __init__(self, numBlocks, IfWin, Time=0):
        self.num = numBlocks
        self.win = IfWin
        self.time = Time
    def addToScore(self):
        database = shelve.open('score')
        database[str(time.gmtime())] = self
        database.close()

#################################################################

def ScoreClassification():
    database = shelve.open('score')
    winNumList = [0]*(maxBlockNum+5)
    lossNumList = [0]*(maxBlockNum+5)
    timeList = [[] for i in range(maxBlockNum+5)]
    for key in database:
        if 0<database[key].num<maxBlockNum+5:
            if database[key].win==True:
                winNumList[database[key].num] += 1
                timeList[database[key].num].append(database[key].time)
            else: lossNumList[database[key].num] += 1
    database.close()
    return winNumList, lossNumList, timeList

def DrawSingleAccuracy(blockNum, accuracy):
        glColor3f(0.5, 0.5, 0.5)
        x = 400 + (blockNum - 7)*50
        y = 170
        glBegin(GL_POLYGON)
        glVertex2f(x-10, y)
        glVertex2f(x+10, y)
        glVertex2f(x+10, y-accuracy*100)
        glVertex2f(x-10, y-accuracy*100)
        glEnd()

def _Mean(numlist): return sum(numlist)/len(numlist)

def _Deviation(numlist):
    return math.sqrt(sum([(i-_Mean(numlist))**2 for i in numlist])/(len(numlist)-1))

def DrawSingleTime(blockNum, timeSeries):
    if len(timeSeries) > 0:
        glColor3f(1,0,0)
        x = 400 + (blockNum - 7)*50
        y = 200 + 100*math.log(_Mean(timeSeries), 10)
        glBegin(GL_POLYGON)
        glVertex2f(x-10, y+10)
        glVertex2f(x+10, y+10)
        glVertex2f(x+10, y-10)
        glVertex2f(x-10, y-10)
        glEnd()

        if len(timeSeries) > 1:
            dev = _Deviation(timeSeries)
            yMax = 200 + 100*math.log(_Mean(timeSeries)+dev, 10)
            yMin = 200 + 100*math.log(max(1, _Mean(timeSeries)-dev), 10)
            glBegin(GL_LINES)
            glVertex2f(x-10, yMax)
            glVertex2f(x+10, yMax)
            glEnd()
            if yMin > 200:
                glBegin(GL_LINES)
                glVertex2f(x-10, yMin)
                glVertex2f(x+10, yMin)
                glEnd()
            glBegin(GL_LINES)
            glVertex2f(x, yMin)
            glVertex2f(x, yMax)
            glEnd()

def DrawAccuracyandTime():
    winNumList, lossNumList, timeList = ScoreClassification()
    for i in range(2, 13):
        if winNumList[i]+lossNumList[i] > 0:
            DrawSingleAccuracy(i, winNumList[i]/(winNumList[i]+lossNumList[i]))
    for i in range(2, 13):
        DrawSingleTime(i, timeList[i])
        
if __name__=='__main__':
    database = shelve.open('score')
    for key in database:
        print(database[key].num, database[key].win, database[key].time)
    database.close()

    print(ScoreClassification())

