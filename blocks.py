from __future__ import division
from __future__ import print_function

from configuration import *

import pyglet
from pyglet.gl import *

def xyz2xy(xyz, View):
    if View == 'Front': return xyz[0], xyz[1]
    elif View == 'Top': return xyz[0], -xyz[2]
    elif View == 'Right': return xyz[1], -xyz[2]

def xy2xyz(xy, View, z=0):
    if View == 'Front': return xy[0], xy[1], z
    elif View == 'Top': return xy[0], z, -xy[1]
    elif View == 'Right': return z, xy[0], -xy[1]

################################################################

class CenterBlock:
    def __init__(self, centerPosition, edgeLength):
        self.center = centerPosition
        self.size = edgeLength
    def shift(self, x=0, y=0, z=0):
        self.center[0] += x
        self.center[1] += y
        self.center[2] += z
    def move(self, x=0, y=0, z=0):
        return CenterBlock([self.center[0]+x, self.center[1]+y, self.center[2]+z], self.size)
    def draw(self, View):
        x, y = xyz2xy(self.center, View)
        glColor3f(0,0,0)
        glBegin(GL_POLYGON)
        glVertex2f(x-self.size/2, y+self.size/2)
        glVertex2f(x+self.size/2, y+self.size/2)
        glVertex2f(x+self.size/2, y-self.size/2)
        glVertex2f(x-self.size/2, y-self.size/2)
        glEnd()
    def draw3D(self, View, z):
        x, y = xyz2xy(self.center, View)
        glColor3f(0,0,0)
        glBegin(GL_POLYGON)
        glVertex3f(*xy2xyz([x-self.size/2, y+self.size/2], View, z))
        glVertex3f(*xy2xyz([x+self.size/2, y+self.size/2], View, z))
        glVertex3f(*xy2xyz([x+self.size/2, y-self.size/2], View, z))
        glVertex3f(*xy2xyz([x-self.size/2, y-self.size/2], View, z))
        glEnd()

def cube2block(cube, Level):
    edge = blockSize[Level]
    dis = edge + blockGap
    return CenterBlock([cube[0]*dis, cube[1]*dis, cube[2]*dis], edge)

def cubeSet2blockSet(cubeSet, Level):
    return {cube2block(cube, Level) for cube in cubeSet}

def showBlockSet(blockSet, View, x, y):
    Label = pyglet.text.Label(View + ' View',
                              font_name='Times New Roman',
                              font_size=viewFontSize,
                              color=(0, 0, 0, 255),
                              x = x,
                              y = y + viewTextOffset,
                              anchor_x='center', anchor_y='center')
    Label.draw()
    for block in blockSet:
        block = CenterBlock.move(block, *xy2xyz([x,y], View))
        block.draw(View)

def showBlockSet3D(blockSet, View, z):
    for block in blockSet:
        block.draw3D(View, z)

################################################################

class EdgeBlock:
    def __init__(self, *vertices):
        self.vertices = vertices
    def printVertex(self):
        for vertex in self.vertices: print(*vertex)
        print('\n')
    def draw(self):
        edgelist = {(0,1), (1,3), (3,2), (2,0),
                    (0,4), (1,5), (3,7), (2,6),
                    (4,5), (5,7), (7,6), (6,4)}
        glColor3f(0,0,0)
        for edgei in edgelist:
            glBegin(GL_LINES)
            for edgeij in edgei:
                glVertex3f(self.vertices[edgeij][0], self.vertices[edgeij][1], self.vertices[edgeij][2])
            glEnd()

 
def centerBlock2edgeBlock(centerBlock):
    vertices = []
    for i in range(0, 8):
        vertices.append([
            centerBlock.center[0] + (-1)**(i%2)*centerBlock.size/2,
            centerBlock.center[1] + (-1)**((i//2)%2)*centerBlock.size/2,
            centerBlock.center[2] + (-1)**((i//4)%2)*centerBlock.size/2])
    return EdgeBlock(*vertices)

def centerSet2edgeSet(blockSet):
    return {centerBlock2edgeBlock(cBlock) for cBlock in blockSet}

def showEdgeSet(edgeSet):
    for block in edgeSet: block.draw()

if __name__ == '__main__':
    edgeBlock = centerBlock2edgeBlock(CenterBlock([0,0,0], 0.6))
    edgeBlock.printVertex()
