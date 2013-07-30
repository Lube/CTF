#! /usr/bin/env python
# Clase Render
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>
import pygame

from pygame.locals import *

WINDOWWIDTH, WINDOWHEIGHT = 300, 200
TILEH, TILEW, GAPSIZE = 32, 64, 1
HALF = WINDOWWIDTH / 2
HTILEH = 0.5 * TILEH
HTILEW = 0.5 * TILEW


class Render():

    def __init__(self, aCamera, aSurface):
        self.Camera = aCamera
        self.Surface = aSurface

    def drawPlaceHolder(self, color, Col, Fila, aCamera = 0):
        if aCamera == 0:
            aCamera = self.Camera
        Y = (Col + Fila) * HTILEH + 32 - aCamera.y
        X = HALF + (Col*HTILEW) - (Fila*HTILEW) - aCamera.x

        pygame.draw.polygon(self.Surface, color, [(X,Y),(X+HTILEW,Y+HTILEH),(X,Y+TILEH),(X-HTILEW, Y+HTILEH)])

    def drawSprite(self, sprite, Col, Fila, aCamera = 0):
        if aCamera == 0:
            aCamera = self.Camera
        Y = (Col + Fila) * HTILEH + 32 - aCamera.y
        X = HALF + (Col*HTILEW) - (Fila*HTILEW) - aCamera.x

        self.Surface.blit(sprite, (X,Y))