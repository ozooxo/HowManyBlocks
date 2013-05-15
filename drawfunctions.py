from __future__ import division
from __future__ import print_function

from configuration import *

import time

import pyglet
from pyglet.gl import *
from pyglet.window import mouse
from pyglet.window import key

def DrawTitle():
    Label = pyglet.text.Label("How Many Blocks?",
                              font_name='Times New Roman',
                              font_size=titleFontSize,
                              color=(63,63,63,63),
                              x=20, y=yScreen-10,
                              anchor_x='left', anchor_y='top')
    Label.draw()

def DrawInitializationProblem():
    glClearColor(255,255,255,255)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    #glViewport(0, 0, xScreen, yScreen)
    DrawTitle()

def DrawInitializationSolution():
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(255,255,255,255)

def DrawInitializationSolution3DBlock(xAngle, yAngle, position='left'):
    glEnable(GL_DEPTH_TEST) 
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity()
    if position=='left': glOrtho(-2*xScreen/7, 5*xScreen/7, -4*yScreen/7, 3*yScreen/7, -xScreen, xScreen)
    if position=='right': glOrtho(-5*xScreen/7, 2*xScreen/7, -4*yScreen/7, 3*yScreen/7, -xScreen, xScreen)
    glRotatef(xAngle, 1, 0, 0)
    glRotatef(yAngle, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

def DrawInitializationSolution2D():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode (GL_PROJECTION) 
    glLoadIdentity() 
    gluOrtho2D(0, xScreen, 0, yScreen) 
    glMatrixMode(GL_MODELVIEW)

    DrawTitle()

##################################################################################

class Timer(pyglet.text.Label):
    def __init__(self, startTime):
        pyglet.text.Label.__init__(self, str('%.1f' % (time.clock()-startTime))+' s',
                                   font_name='Times New Roman',
                                   font_size=navigatorFontSize,
                                   color=(127, 127, 127, 255),
                                   bold=True,
                                   x=xScreen-navigatorSpace,
                                   y=yScreen-navigatorSpace,
                                   anchor_x='right', anchor_y='top')

class Button(pyglet.text.Label):
    def boundary(self):
        if self.anchor_x=='center':
            self.xMin = self.x - 0.5*self.font_size*len(self.text)
            self.xMax = self.x + 0.5*self.font_size*len(self.text)
        elif self.anchor_x=='left':
            self.xMin = self.x
            self.xMax = self.x + 0.8*self.font_size*len(self.text)
        elif self.anchor_x=='right':
            self.xMin = self.x - 0.8*self.font_size*len(self.text)
            self.xMax = self.x
        
        if self.anchor_y=='center':
            self.yMin = self.y - 0.6*self.font_size
            self.yMax = self.y + 0.6*self.font_size
        if self.anchor_y=='bottom':
            self.yMin = self.y - 0.1*self.font_size
            self.yMax = self.y + 1.1*self.font_size
            
    def drawWithMouseOn(self, mousePos):
        self.boundary()
        if (self.xMin < mousePos[0] < self.xMax) and (self.yMin < mousePos[1] < self.yMax):
            colorBackup = self.color
            self.color = (225, 0, 0, 255)
            self.draw()
            self.color = colorBackup
        else: self.draw()

    def clickNext(self, mouseClickPos, playStatus, nextStatus):
        self.boundary()
        if (self.xMin < mouseClickPos[0] < self.xMax) and (self.yMin < mouseClickPos[1] < self.yMax):
            playStatus[0] = nextStatus
            return True
        else: return False

class ButtonNavigator(Button):
    def __init__(self, text, LeftCenterRight):
        if LeftCenterRight=='left': xPosition = navigatorSpace
        elif LeftCenterRight=='center': xPosition = xScreen/2
        elif LeftCenterRight=='right': xPosition = xScreen-navigatorSpace
        elif isinstance(LeftCenterRight, int):
            xPosition = LeftCenterRight
            LeftCenterRight = 'center'
        pyglet.text.Label.__init__(self, str(text),
                                   font_name='Times New Roman',
                                   font_size=navigatorFontSize,
                                   color=(127, 127, 127, 255),
                                   bold=True,
                                   x=xPosition,
                                   y=navigatorSpace,
                                   anchor_x=LeftCenterRight, anchor_y='bottom')

def DrawNavigator(text, LeftCenterRight, mousePos, mouseClickPos, playStatus, nextStatus):
    ButtonTmp = ButtonNavigator(text, LeftCenterRight)
    ButtonTmp.drawWithMouseOn(mousePos)
    return ButtonTmp.clickNext(mouseClickPos, playStatus, nextStatus)
