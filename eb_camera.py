#! /usr/bin/env python
# Clase Camera
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

WINDOWWIDTH, WINDOWHEIGHT = 300, 200
TILEH, TILEW, GAPSIZE = 32, 64, 1
BOARDWIDTH = 15
HALF = WINDOWWIDTH / 2
HTILEH = 0.5 * TILEH
HTILEW = 0.5 * TILEW

class Camera(object):
    x = 0
    y = 0
    xyTile = 0,0
    mode = ''
    xRange = 0
    yRange = 0

    def __init__(self, aMode, aPos):
        self.x = 0
        self.y = 0
        self.xyTile = 0,0
        self.mode = aMode

        if self.mode == 'DYNAMIC':
            self.xyTile = copy.copy(aPos)
            self.xRange, self.yRange = 15,15
        else:
            self.xRange, self.yRange = 15,15
            self.xyTile = aPos


    def update(self, aPos):
        if self.mode == 'DYNAMIC':
            if aPos[0] > (self.xyTile[0] + (self.xRange - 2)):
                self.xyTile[0] += 1
            elif aPos[0] < (self.xyTile[0] - (self.xRange - 1)):
                self.xyTile[0] -= 1
            elif aPos[1] > (self.xyTile[1] + (self.yRange - 2)):
                self.xyTile[1] += 1
            elif aPos[1] < (self.xyTile[1] - (self.yRange - 1)):
                self.xyTile[1] -= 1
        if self.mode == 'STATIC':
                self.xyTile = aPos

        self.x = HALF + (self.xyTile[0]*HTILEW) - (self.xyTile[1]*HTILEW)
        self.y =(self.xyTile[0] + self.xyTile[1]) * HTILEH + 32
        #tuple(map(int,getVertsOfTile(aChar.pos[0], aChar.pos[1])))
        self.x, self.y = (self.x - WINDOWWIDTH/2), (self.y - WINDOWHEIGHT/2)
