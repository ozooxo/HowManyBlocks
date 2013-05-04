from __future__ import division
from __future__ import print_function

import random

def BlockSet2BoundarySet(BlockSet):
    BoundarySet = set()
    for Block in BlockSet:
        BoundarySet.add((Block[0]+1, Block[1], Block[2]))
        BoundarySet.add((Block[0]-1, Block[1], Block[2]))
        BoundarySet.add((Block[0], Block[1]+1, Block[2]))
        BoundarySet.add((Block[0], Block[1]-1, Block[2]))
        BoundarySet.add((Block[0], Block[1], Block[2]+1))
        BoundarySet.add((Block[0], Block[1], Block[2]-1))
    return BoundarySet - BlockSet

#print(BlockSet2BoundarySet({(0,0,0), (1,0,0)}))

#def NewBlock2BoundarySet(NewBlock, BlockSet, oldBoundarySet):
#    BoundarySet = oldBoundarySet.union(BlockSet2BoundarySet({NewBlock}))
#    return BoundarySet - BlockSet

def RandomBlockGenerator(numBlocks):
    BlockSet = {(0,0,0)}
    while len(BlockSet) < numBlocks:
        NewBlock = random.choice(list(BlockSet2BoundarySet(BlockSet)))
        BlockSet.add(NewBlock)
    return BlockSet

#print(RandomBlockGenerator(4))

def BlockSet2oneDimProjection(BlockSet):
    xSet, ySet, zSet = set(), set(), set()
    for Block in BlockSet:
        xSet.add(Block[0])
        ySet.add(Block[1])
        zSet.add(Block[2])
    return (xSet, ySet, zSet)

def BlockSet2twoDimProjection(BlockSet):
    xySet, yzSet, xzSet = set(), set(), set()
    for Block in BlockSet:
        xySet.add((Block[0], Block[1]))
        yzSet.add((Block[1], Block[2]))
        xzSet.add((Block[0], Block[2]))
    return (xySet, yzSet, xzSet)

#print(BlockSet2twoDimProjection(RandomBlockGenerator(4)))

def RandomBlockSet2FilledBlockSet(RandomBlockSet):
    xSet, ySet, zSet = BlockSet2oneDimProjection(RandomBlockSet)
    xySet, yzSet, xzSet = BlockSet2twoDimProjection(RandomBlockSet)

    FilledBlockSet = set()
    xyz_grid = {(x, y, z) for x in xSet for y in ySet for z in zSet}
    for (x,y,z) in xyz_grid:
        if ((x,y) in xySet) and ((y,z) in yzSet) and ((x,z) in xzSet):
            FilledBlockSet.add((x,y,z))
    return FilledBlockSet

#print(RandomBlockSet2FilledBlockSet(RandomBlockGenerator(6)))
