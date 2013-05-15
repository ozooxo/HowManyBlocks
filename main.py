from __future__ import division
from __future__ import print_function

import random
import math

from configuration import *
from algorithm import GenerateCubeSet
from drawfunctions import *
from blocks import *
from solution import *
from recordscore import *

##################################################################################

import pyglet
from pyglet.gl import *
from pyglet.window import mouse

window = pyglet.window.Window(xScreen, yScreen)

mousePos = (0, 0)
mouseClickPos = (0, 0)

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mousePos
    mousePos = (x, y)

@window.event
def on_mouse_press(x, y, button, modifiers):
    global mouseClickPos
    mouseClickPos = (x, y)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global xAngle, yAngle
    xAngle += -0.3*dy
    yAngle += 0.3*dx

@window.event
def on_mouse_release(x, y, button, modifiers):
    global mouseClickPos
    mouseClickPos = (0, 0)

assumption_concave_image = pyglet.resource.image("assumption_concave.png")
assumption_concave_sprite = pyglet.sprite.Sprite(img=assumption_concave_image,x=0,y=100)
assumption_views_image = pyglet.resource.image("assumption_views.png")
assumption_views_sprite = pyglet.sprite.Sprite(img=assumption_views_image,x=0,y=100)
score_background_image = pyglet.resource.image("score_background.png")
score_background_sprite = pyglet.sprite.Sprite(img=score_background_image,x=0,y=0)

#################################################################
    
playStatus =  ['Initialization'] # ['Score'] # ['ShowProblem'] #

def GenerateBlockSet(startNum, level):
    cubeSet = GenerateCubeSet(startNum)
    return cubeSet2blockSet(cubeSet, level)

blockSet, solutionSet, edgeSet = [], [], []
level, wrongNum, startTime = 'Medium', None, 0
xAngle, yAngle = 30, -30

def Level2StartNum(level):
    return random.choice(blockNumber[level])

def GenerateAll(startNum, level, numSolution):
    global blockSet, solutionSet, edgeSet, wrongNum, startTime
    
    blockSet = GenerateBlockSet(startNum, level)
    edgeSet = centerSet2edgeSet(blockSet)
    solutionSet = GenerateSolutionSet(len(blockSet), numSolution)
    wrongNum = None
    startTime = time.clock()

GenerateAll(Level2StartNum(level), level, blockChoiceNumber[level])

#################################################################

@window.event
def on_draw():
    global blockSet, solutionSet, edgeSet, level, wrongNum, startTime, xAngle, yAngle
    global mouseClickPos

    if playStatus[0] == 'Initialization':
        DrawInitializationProblem()
        assumption_views_sprite.draw()
        if DrawNavigator('NEXT >>', 'right', mousePos, mouseClickPos, playStatus, 'Assumption'): mouseClickPos = (0, 0)

    elif playStatus[0] == 'Assumption':
        DrawInitializationProblem()
        assumption_concave_sprite.draw()
        if DrawNavigator('NEXT >>', 'right', mousePos, mouseClickPos, playStatus, 'Score'): mouseClickPos = (0, 0)

    elif playStatus[0] == 'Score':
        DrawInitializationProblem()
        score_background_sprite.draw()
        DrawAccuracyandTime()
        positionList = {'Easy': 280, 'Medium': 360, 'Hard': 440, 'Expert': 517}
        for key in positionList:
            if DrawNavigator('-'+key+'-', positionList[key], mousePos, mouseClickPos, playStatus, 'ShowProblem'):
                level = key
                GenerateAll(Level2StartNum(level), level, blockChoiceNumber[level])
                mouseClickPos = (0, 0)

    elif playStatus[0] == 'ShowProblem':
        DrawInitializationProblem()
        showBlockSet(blockSet, 'Front', x=xScreen/2-ViewsDistance, y=viewHeight)
        showBlockSet(blockSet, 'Top', x=xScreen/2, y=viewHeight)
        showBlockSet(blockSet, 'Right', x=xScreen/2+ViewsDistance, y=viewHeight)
        
        wrongNum = DrawPossibleNumbers(solutionSet, mousePos, mouseClickPos, playStatus)
        if wrongNum != None:
            if wrongNum == len(blockSet):
                wrongNum = None
                OneTaskScore(len(blockSet), True, time.clock()-startTime).addToScore()
            else: OneTaskScore(len(blockSet), False, time.clock()-startTime).addToScore()
            xAngle, yAngle = 30, -30

        if DrawNavigator('GIVE UP', 'center', mousePos, mouseClickPos, playStatus, 'ShowSolution'):
            OneTaskScore(len(blockSet), False, time.clock()-startTime).addToScore()
            mouseClickPos = (0, 0)
            xAngle, yAngle = 30, -30

        Timer(startTime).draw()
        if DrawNavigator('<< BACK', 'left', mousePos, mouseClickPos, playStatus, 'Score'): mouseClickPos = (0, 0)

    elif playStatus[0] == 'ShowSolution':

        DrawInitializationSolution()

        DrawInitializationSolution3DBlock(xAngle, yAngle, position='left')
        showEdgeSet(edgeSet)

        DrawInitializationSolution3DBlock(xAngle, yAngle, position='right')
        showEdgeSet(edgeSet)
        showBlockSet3D(blockSet, 'Top', 130) 
        showBlockSet3D(blockSet, 'Front', 130)
        showBlockSet3D(blockSet, 'Right', 130)

        DrawInitializationSolution2D()

        DrawSolutionNumbers(solutionSet, len(blockSet), wrongNum)
        if DrawNavigator('NEXT TASK >>', 'right', mousePos, mouseClickPos, playStatus, 'ShowProblem'):
            GenerateAll(Level2StartNum(level), level, blockChoiceNumber[level])
            mouseClickPos = (0, 0)

        ButtonNavigator('< Drag to Change View Angle >', 'center').draw()

        if DrawNavigator('<< BACK', 'left', mousePos, mouseClickPos, playStatus, 'Score'): mouseClickPos = (0, 0)


    """
    DrawInitializationSolution()
    showEdgeSet(edgeSet)
    """

pyglet.app.run()
