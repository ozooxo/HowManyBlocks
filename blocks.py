from __future__ import division
from __future__ import print_function

import random
import math

from algorithm import *

# global variables
xySet, yzSet, xzSet = set(), set(), set()
ifStart = True
ifSolved = False
Score = 0
numBlocks = 0
PossibleNumSet = []
wrongPos = None

def GenerateNewGame():
    global xySet, yzSet, xzSet, numBlocks
    if Score > 0: RandomNumBlocks = random.randint(1+int(1.5*math.sqrt(Score)),1+int(2.4*math.sqrt(Score)))
    else: RandomNumBlocks = 1
    RandomBlockSet = RandomBlockGenerator(RandomNumBlocks)
    FilledBlockSet = RandomBlockSet2FilledBlockSet(RandomBlockSet)
    xySet, yzSet, xzSet = BlockSet2twoDimProjection(FilledBlockSet)
    numBlocks = len(FilledBlockSet)

GenerateNewGame()

def GenerateSolutionSet():
    global PossibleNumSet
    randomMin = numBlocks - random.randint(0,4)
    if randomMin < 1: randomMin = 1
    randomMax = randomMin + 5
    PossibleNumSet = range(randomMin, randomMax)

GenerateSolutionSet()

##################################################################################

import pyglet
from pyglet.gl import *
from pyglet.window import mouse

mousePos = (0, 0)
window = pyglet.window.Window(640, 480)

def DrawLabel(xCenter, yCenter, words, size, textColor=(255, 255, 255, 255)):
    Label = pyglet.text.Label(words,
                              font_name='Times New Roman',
                              font_size=size,
                              color=textColor,
                              x=xCenter, y=yCenter,
                              anchor_x='center', anchor_y='center')
    Label.draw()

def DrawTwoDimBlock(xCenter, yCenter, Size):
    glBegin(GL_POLYGON)
    glVertex2f(xCenter-Size/2, yCenter+Size/2)
    glVertex2f(xCenter+Size/2, yCenter+Size/2)
    glVertex2f(xCenter+Size/2, yCenter-Size/2)
    glVertex2f(xCenter-Size/2, yCenter-Size/2)
    glEnd()

def DrawTwoDimSet(xySet, xCenter, yCenter, BlockSize, words, size):
    for xy in xySet:
        DrawTwoDimBlock(xCenter+xy[0]*BlockSize, yCenter+xy[1]*BlockSize, BlockSize)
    DrawLabel(xCenter, 7*window.height//10, words, size, (127, 127, 127, 255))

def DrawCrossSign(xCenter, yCenter):
    glBegin(GL_POLYGON)
    glVertex2f(xCenter-12-2, yCenter-12+2)
    glVertex2f(xCenter-12+2, yCenter-12-2)
    glVertex2f(xCenter+12+2, yCenter+12-2)
    glVertex2f(xCenter+12-2, yCenter+12+2)
    glEnd()
    glBegin(GL_POLYGON)
    glVertex2f(xCenter-12-2, yCenter+12-2)
    glVertex2f(xCenter-12+2, yCenter+12+2)
    glVertex2f(xCenter+12+2, yCenter-12+2)
    glVertex2f(xCenter+12-2, yCenter-12-2)
    glEnd()

def DrawPossibleSolutions(xCenter, yCenter):
    global ifSolved, Score, wrongPos

    for i, numPossible in enumerate(PossibleNumSet):
        DrawLabel(xCenter+(i+0.5-len(PossibleNumSet)/2)*50, yCenter, str(numPossible), 24)
    
    if ifSolved == False:
        i = PossibleNumSet.index(numBlocks)
        if (xCenter+(i+0.5-len(PossibleNumSet)/2)*50-25)<mousePos[0]<(xCenter+(i+0.5-len(PossibleNumSet)/2)*50+25) and (yCenter-15)<mousePos[1]<(yCenter+15):
            wrongPos = None
            ifSolved = True
            Score += 1
        elif (xCenter+(0.5-len(PossibleNumSet)/2)*50-25)<mousePos[0]<(xCenter+(len(PossibleNumSet)/2-0.5)*50+25) and (yCenter-15)<mousePos[1]<(yCenter+15):
            wrongPos = mousePos[:]
            ifSolved = True
            Score -= 1

    if ifSolved == True:
        i = PossibleNumSet.index(numBlocks)
        DrawLabel(xCenter+(i+0.5-len(PossibleNumSet)/2)*50, yCenter, str(numBlocks), 24, (0, 255, 0, 255))
        if wrongPos: DrawCrossSign(*wrongPos)

def DrawNext():
    global ifStart, ifSolved
    
    DrawLabel(window.width-60, 25, 'NEXT >>>', 12, (127, 127, 127, 255))
    if (window.width-105)<mousePos[0]<(window.width-45) and 15<mousePos[1]<35:
        ifStart = False
        ifSolved = False
        GenerateNewGame()
        GenerateSolutionSet()

@window.event
def on_mouse_press(x, y, button, modifiers):
    global mousePos
    mousePos = (x, y)

@window.event
def on_mouse_release(x, y, button, modifiers):
    global mousePos
    mousePos = (0, 0)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    DrawLabel(window.width//2, 5*window.height//6, 'How Many Blocks?', 36)

    if ifStart == True:
        DrawLabel(window.width//2, 7*window.height//10,      'Important Assumption: If a position is hidden by', 18, (127, 127, 127, 255))
        DrawLabel(window.width//2, 7*window.height//10 - 32, 'other blocks in all three possible views, There is', 18, (127, 127, 127, 255))
        DrawLabel(window.width//2, 7*window.height//10 - 64, 'always a block there. Roughly in other word, there', 18, (127, 127, 127, 255))
        DrawLabel(window.width//2, 7*window.height//10 - 96, 'is no concave configurations.', 18, (127, 127, 127, 255))
    else:
        DrawTwoDimSet(xzSet, window.width//5, window.height//2, 20, 'Front View', 18)
        DrawTwoDimSet(xySet, window.width//2, window.height//2, 20, 'Top View', 18)
        DrawTwoDimSet(yzSet, 4*window.width//5, window.height//2, 20, 'Right View', 18)

        #DrawLabel(window.width//2, 5*window.height//8, str(numBlocks), 24)

        DrawPossibleSolutions(window.width//2, window.height//4)

        DrawLabel(55, 25, 'SCORE: '+str(Score), 12, (127, 127, 127, 255))

    DrawNext()

pyglet.app.run()
