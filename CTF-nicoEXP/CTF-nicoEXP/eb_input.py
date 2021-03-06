#! /usr/bin/env python
# Clase Input
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

import pygame
from eb_render import *
from pygame.locals import *

WINDOWWIDTH, WINDOWHEIGHT = 800, 600
DOWN, RIGHT, UP, LEFT = (1,1), (1,-1), (-1,-1), (-1,1)
NE, SE, NO, SO = (0,-1), (1,0), (-1,0), (0,1)
dKey2Dir = {K_d: RIGHT, K_s:DOWN, K_a:LEFT, K_w:UP}

class Input():
    def __init__(self):
        self.Commands = []
        self.Order = (0,0)
        self.CameraOrder = None
        self.Quit = False
        self.ChangeSignal = False
        self.Click = False
        self.nSkill = None

    def update(self):
        self.ChangeSignal = False
        self.WalkRun = False
        self.Wait = False
        self.Rotate = False
        self.Click = False
        self.nSkill = None
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
                if pygame.mouse.get_pressed()[0]:
                    self.Click = True
                if anEvent.key == K_1:
                    self.nSkill = 0
                if anEvent.key == K_2:
                    self.nSkill = 1

            if anEvent.type == pygame.KEYUP:
                if anEvent.key in dKey2Dir.keys():
                    self.remove(dKey2Dir[anEvent.key])
            if anEvent.type == MOUSEBUTTONDOWN:
                self.Click = True
            if anEvent.type == MOUSEMOTION:
                X, Y = pygame.mouse.get_pos()
                if X < 50:
                    self.CameraOrder = LEFT
                elif X > (WINDOWWIDTH - 50):
                    self.CameraOrder = RIGHT
                elif Y < 50:
                    self.CameraOrder = UP
                elif Y > (WINDOWHEIGHT - 50):
                    self.CameraOrder = DOWN
                else:
                    self.CameraOrder = None


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
        COL, FILA = self.realTileMouse()
    
        COL = int(COL)
        FILA = int(FILA)

        return COL, FILA
    
    def realTileMouse(self):
        X, Y = pygame.mouse.get_pos()

        COL, FILA = CoordsToTiles(X,Y)
        return (COL, FILA) |x| (-3,-3)
    
    def realMouse(self):
        return pygame.mouse.get_pos()
    

    def mouseDirection(self, char):
        cX, cY = char.Posicion
        mX, mY = self.mouse()
        if mX == None:
            mX = 0
        if mY == None:
            mY = 0
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
        return self.facing

def CoordsToTiles(X,Y):
    FILA = (Y - (X*TILEH/TILEW) + (HALF*TILEH/TILEW)) / HTILEH / 2
    COL = (X - HALF + (FILA*HTILEW)) / HTILEW
    return COL, FILA
