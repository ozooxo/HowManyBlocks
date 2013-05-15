from __future__ import division
from __future__ import print_function

import random
from configuration import *
from drawfunctions import Button

import pyglet

def GenerateSolutionSet(numBlocks, numPossibilities):
    randomMin = numBlocks - random.randint(0,numPossibilities-1)
    if randomMin < minBlockNum: randomMin = minBlockNum
    #if randomMin > maxBlockNum-numPossibilities+1: randomMin = maxBlockNum-numPossibilities+1
    randomMax = randomMin + numPossibilities
    return range(randomMin, randomMax)

##################################################################################

class ButtonSolution(Button):
    def __init__(self, number, xOffset, solveStatus=False):
        if solveStatus==False: textColor = (0, 0, 0, 255)
        elif solveStatus=='Correct': textColor = (0, 191, 0, 255)
        elif solveStatus=='Wrong': textColor = (255, 0, 0, 255)
        pyglet.text.Label.__init__(self, str(number),
                                   font_name='Times New Roman',
                                   font_size=solutionFontSize,
                                   bold=True,
                                   color=textColor,
                                   x=xScreen/2 + xOffset,
                                   y=yScreen/2+solutionTextOffset,
                                   anchor_x='center', anchor_y='center')


def DrawPossibleNumbers(solutionSet, mousePos, mouseClickPos, playStatus):
    for i, numPossible in enumerate(solutionSet):
        ButtonTmp = ButtonSolution(numPossible, (i+0.5-len(solutionSet)/2)*(solutionFontSize*2))
        ButtonTmp.drawWithMouseOn(mousePos)
        if ButtonTmp.clickNext(mouseClickPos, playStatus, 'ShowSolution')==True: return numPossible # return clickNum

def DrawSolutionNumbers(solutionSet, correctNum, wrongNum=None):
    for i, numPossible in enumerate(solutionSet):
        ButtonSolution(numPossible, (i+0.5-len(solutionSet)/2)*(solutionFontSize*2)).draw()
    i = solutionSet.index(correctNum)
    ButtonSolution(correctNum, (i+0.5-len(solutionSet)/2)*(solutionFontSize*2), solveStatus='Correct').draw()
    if wrongNum != None:
        i = solutionSet.index(wrongNum)
        ButtonSolution(wrongNum, (i+0.5-len(solutionSet)/2)*(solutionFontSize*2), solveStatus='Wrong').draw()

if __name__=='__main__':
    print(GenerateSolutionSet(7, 4))
