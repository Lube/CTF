#! /usr/bin/env python
# Clase Input
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

import pygame
from eb_render import *
from pygame.locals import *

WINDOWWIDTH, WINDOWHEIGHT = 800, 600
UP, RIGHT, DOWN, LEFT = (1,1), (1,-1), (-1,-1), (-1,1)
NE, SE, NO, SO = (0,-1), (1,0), (-1,0), (0,1)
dKey2Dir = {275: RIGHT, 273:DOWN, 276:LEFT, 274:UP}

class Input():
    def __init__(self):
        self.facing = RIGHT
        self.Commands = []
        self.Order = (0,0)
        self.CameraOrder = None
        self.Quit = False
        self.ChangeSignal = False
        self.Click = False
        self.Rotate = False

    def update(self):
        self.ChangeSignal = False
        self.WalkRun = False
        self.Wait = False
        self.Rotate = False
<<<<<<< HEAD
=======
        self.Click = False
>>>>>>> hey yo

        for anEvent in pygame.event.get():
            if anEvent.type == pygame.KEYDOWN:
                if anEvent.key in dKey2Dir.keys():
                    self.append(dKey2Dir[anEvent.key])
                if anEvent.key == K_ESCAPE:
                    self.Quit = True
                if anEvent.key == K_TAB:
                    self.ChangeSignal = True
                if anEvent.key == K_LSHIFT:
                    self.WalkRun = True
                if anEvent.key == K_SPACE:
                    self.Wait = True
                if anEvent.key == K_LCTRL:
                    self.Rotate = True
<<<<<<< HEAD
=======
                if pygame.mouse.get_pressed()[0]:
                    self.Click = True
>>>>>>> hey yo
            if anEvent.type == pygame.KEYUP:
                if anEvent.key in dKey2Dir.keys():
                    self.remove(dKey2Dir[anEvent.key])
            if anEvent.type == MOUSEBUTTONDOWN:
                print "CLICK" , anEvent.pos
            if anEvent.type == MOUSEMOTION:
                X, Y = pygame.mouse.get_pos()
                if X < 50:
                    self.CameraOrder = LEFT
                elif X > (WINDOWWIDTH - 50):
                    self.CameraOrder = RIGHT
                elif Y < 50:
                    self.CameraOrder = DOWN
                elif Y > (WINDOWHEIGHT - 50):
                    self.CameraOrder = UP
                else:
                    self.CameraOrder = None
        print self.mouse()


    def updateOrder(self):
        xAcum, yAcum = 0, 0
        for Command in self.Commands:
            xAcum += Command[0]
            yAcum += Command[1]

        if xAcum == 2:
            xAcum = 1
        elif xAcum == -2:
            xAcum = -1

        if yAcum == 2:
            yAcum = 1
        elif yAcum == -2:
            yAcum = -1

        self.Order = xAcum, yAcum

    def append(self, aCommand):
        self.Commands.append(aCommand)
        self.updateOrder()

    def remove(self, aCommand):
        assert len(self.Commands) > 0
        self.Commands.remove(aCommand)
        self.updateOrder()

    def empty(self):
        return len(self.Commands) == 0

    def mouse(self):
<<<<<<< HEAD
        x, y = pygame.mouse.get_pos()
        pos = (int(x/(TILEW-(GAPSIZE*BOARDWIDTH))),int(y/(TILEH-(GAPSIZE*BOARDWIDTH))))
        return pos
=======
        X, Y = pygame.mouse.get_pos()
        
        COL, FILA = CoordsToTiles(X,Y)
        
        if (COL < 0):
            COL = None
            FILA = None
        else:
            COL = int(COL)
            
        if (FILA < 0):
            COL = None
            FILA = None
        else:
            FILA = int(FILA)
            
        return COL, FILA
>>>>>>> hey yo

    def mouseDirection(self, char):
        cX, cY = char.posicion
        mX, mY = self.mouse()
        if mX > cX:
            if abs(mX+cX) > abs(cY+mY):
                self.facing = RIGHT
        else:
            if abs(mX+cX) > abs(cY+mY):
                self.facing = LEFT
        if mY > cY:
            if abs(mY+cY) > abs(cX+mX):
                self.facing = DOWN
        else:
            if abs(mY+cY) > abs(cX+mX):
                self.facing = UP
<<<<<<< HEAD
=======

def CoordsToTiles(X,Y):
    FILA = (Y - 32 - (X*TILEH/TILEW) + (HALF*TILEH/TILEW)) / HTILEH / 2
    COL = (X - HALF + (FILA*HTILEW)) / HTILEW
    return COL, FILA
>>>>>>> hey yo
