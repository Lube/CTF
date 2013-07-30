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

PHEIGHT = 16 
PHHEIGHT = 8 
PHWIDTH = 16

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)
    
x = Infix(lambda a,b:tuple([x+y for x, y in zip(a, b)]))

y = Infix(lambda a,b:tuple([a*y for y in b]))


class Render():

    def __init__(self, aCamera, aSurface):
        self.Camera = aCamera
        self.Surface = aSurface
        
    def drawLine(self, color, Origen, Destino, aCamera = 0):
        if aCamera == 0:
            aCamera = self.Camera
        O = Tiles2Coords(Origen) |x| (-aCamera.x, -aCamera.y)
        D = Tiles2Coords(Destino)|x| (-aCamera.x, -aCamera.y)
        
        pygame.draw.line(self.Surface, color, O, D, 6)
    

    def drawPlaceHolder(self, color, Col, Fila, aCamera = 0, source = 'terreno'):
        if aCamera == 0:
            aCamera = self.Camera

        X, Y = Tiles2Coords((Col, Fila))
        X, Y = X-aCamera.x, Y-aCamera.y
        if (X<aCamera.xRange and X>-100 and Y>-100 and Y<aCamera.yRange):
            if source == 'terreno':
                pygame.draw.polygon(self.Surface, color, [(X,Y),(X+HTILEW,Y+HTILEH),(X,Y+TILEH),(X-HTILEW, Y+HTILEH)])
            else:
                pygame.draw.polygon(self.Surface, color, [(X,Y),(X+PHWIDTH,Y+PHHEIGHT),(X,Y+PHEIGHT),(X-PHWIDTH, Y+PHHEIGHT)])
        

    def drawSprite(self, sprite, Col, Fila, aCamera = 0):
        if aCamera == 0:
            aCamera = self.Camera
        
        X, Y = Tiles2Coords((Col, Fila)) |x| (-aCamera.x, -aCamera.y)

        self.Surface.blit(sprite, (X,Y))
        
def Tiles2Coords((Col, Fila)):
    Y = (Col + Fila) * HTILEH 
    X = HALF + (Col*HTILEW) - (Fila*HTILEW)
    
    return X,Y