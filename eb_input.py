#! /usr/bin/env python
# Clase Input
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

import pygame
from pygame.locals import *

UP, RIGHT, DOWN, LEFT = (1,1), (1,-1), (-1,-1), (-1,1)
NE, SE, NO, SO = (0,-1), (1,0), (-1,0), (0,1)
dKey2Dir = {275: RIGHT, 273:DOWN, 276:LEFT, 274:UP}

class Input():
    def __init__(self):
        self.Commands = []
        self.Order = (0,0)
        self.Quit = False
        self.ChangeSignal = False

    def update(self):
        self.ChangeSignal = False
        self.WalkRun = False
        self.Wait = False
        
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
            if anEvent.type == pygame.KEYUP:
                if anEvent.key in dKey2Dir.keys():
                    self.remove(dKey2Dir[anEvent.key])


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

