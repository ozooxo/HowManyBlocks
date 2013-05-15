from __future__ import division
from __future__ import print_function

import random

__all__ = ["GenerateCubeSet"]

def CubeSet2BoundarySet(CubeSet):
    BoundarySet = set()
    for Cube in CubeSet:
        BoundarySet.add((Cube[0]+1, Cube[1], Cube[2]))
        BoundarySet.add((Cube[0]-1, Cube[1], Cube[2]))
        BoundarySet.add((Cube[0], Cube[1]+1, Cube[2]))
        BoundarySet.add((Cube[0], Cube[1]-1, Cube[2]))
        BoundarySet.add((Cube[0], Cube[1], Cube[2]+1))
        BoundarySet.add((Cube[0], Cube[1], Cube[2]-1))
    return BoundarySet - CubeSet

def RandomCubeGenerator(numCubes):
    CubeSet = {(0,0,0)}
    while len(CubeSet) < numCubes:
        NewCube = random.choice(list(CubeSet2BoundarySet(CubeSet)))
        CubeSet.add(NewCube)
    return CubeSet

def CubeSet2oneDimProjection(CubeSet):
    xSet, ySet, zSet = set(), set(), set()
    for Cube in CubeSet:
        xSet.add(Cube[0])
        ySet.add(Cube[1])
        zSet.add(Cube[2])
    return (xSet, ySet, zSet)

def CubeSet2twoDimProjection(CubeSet):
    xySet, yzSet, xzSet = set(), set(), set()
    for Cube in CubeSet:
        xySet.add((Cube[0], Cube[1]))
        yzSet.add((Cube[1], Cube[2]))
        xzSet.add((Cube[0], Cube[2]))
    return (xySet, yzSet, xzSet)

def RandomCubeSet2FilledCubeSet(RandomCubeSet):
    xSet, ySet, zSet = CubeSet2oneDimProjection(RandomCubeSet)
    xySet, yzSet, xzSet = CubeSet2twoDimProjection(RandomCubeSet)

    FilledCubeSet = set()
    xyz_grid = {(x, y, z) for x in xSet for y in ySet for z in zSet}
    for (x,y,z) in xyz_grid:
        if ((x,y) in xySet) and ((y,z) in yzSet) and ((x,z) in xzSet):
            FilledCubeSet.add((x,y,z))
    return FilledCubeSet

def GenerateCubeSet(startNum):
    return RandomCubeSet2FilledCubeSet(RandomCubeGenerator(startNum))
