#! /usr/bin/env python
# Clase Turno, Action, Movimiento, AutoAtaque
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

from eb_lectormapa import Mapa
from eb_input import *
import math

RED   =     (160, 25 ,  25 )

class Action():
    pass

class Skillshot(Action):
    Speed = 2
    Range = 5 
    PlaceHolderColor = RED
    Persistent = True
    
    def __init__(self, (Origen, Destino)):
        self.Origen = Origen
        self.Destino = Destino
        self.Pos = Origen
        self.Step = 0
        self.vTrayectoria = self.Destino[0] - self.Origen[0], self.Destino[1] - self.Origen[1]
        self.Over = False
        self.HitBox = HitBox(self.Pos, (0.5,0.5))
        Mag = math.sqrt(sum([self.vTrayectoria[i] ** 2 for i in [0,1]]))
        self.vTrayectoria = [self.vTrayectoria[i]/Mag for i in [0,1]]
        
    def play(self):
        self.Step += 0.5
        X = self.vTrayectoria[0]/2
        Y = self.vTrayectoria[1]/2
        
        #X, Y = X, Y
        self.Pos = self.Pos |x| (X,Y)
        self.Pos = round(self.Pos[0],1), round(self.Pos[1],1)
        self.HitBox.update(self.Pos)
        if self.Step >= self.Range:
            self.Over = True
        
    def getStringInfo(self):
        toSend = ''
        toSend = self.__class__.__name__ \
        + ',' + str(self.Origen[0]) + ',' + str(self.Origen[1])\
        + ',' + str(self.Destino[0]) + ','  + str(self.Destino[1]) + '|'
        return toSend
        
        
    def update(self, Origen, Destino):
        self.Origen = Origen 
        self.Destino = Destino
        self.vTrayectoria = self.Destino[0] - self.Origen[0], self.Destino[1] - self.Origen[1]
        
        Mag = math.sqrt(sum([self.vTrayectoria[i] ** 2 for i in [0,1]]))
        self.vTrayectoria = [self.vTrayectoria[i]/Mag for i in [0,1]]
        
       
    def draw(self, aRender, Mode = 'playing'):
            if Mode == 'planning':           
                aRender.drawLine(self.PlaceHolderColor, self.Origen, self.Destino)
            else:
                aRender.drawPlaceHolder(self.PlaceHolderColor, self.Pos[0], self.Pos[1], 0, 'char')


class Walk(Action):
    Persistent = False
    def __init__(self, Pos):
        self.Pos = Pos
    
    def getStringInfo(self):
        toSend = ''
        toSend = self.__class__.__name__ + ',' + str(self.Pos[0]) + ',' + str(self.Pos[1]) + '|'
        return toSend
        
    def play(self, aChar):
        aChar.Posicion = self.Pos
        aChar.HitBox.update(self.Pos)



class Run(Action):
    Persistent = False
    def __init__(self, Pos):
        self.Pos = Pos
    
    def getStringInfo(self):
        toSend = ''
        toSend = self.__class__.__name__ + ',' + str(self.Pos[0]) + ',' + str(self.Pos[1]) + '|'
        return toSend
    
    def play(self, aChar):
        aChar.Posicion = self.Pos
        aChar.HitBox.update(self.Pos)


class Wait(Action):
    Persistent = False
    Pos = (0,0)
    def __init__(self, Pos):
        self.Pos = Pos
        
    def getStringInfo(self):
        toSend = ''
        toSend = self.__class__.__name__ + ',' + str(self.Pos[0]) + ',' + str(self.Pos[1]) + '|'
        return toSend

    def play(self, aChar):
        aChar.Posicion = self.Pos



"""H = (Destino[1] - self.Char.Posicion[1]) ** 2 + (Destino[0] - self.Char.Posicion[0]) ** 2
        H = math.sqrt(H)
        O = Destino[1] - self.Char.Posicion[1]
        A = Destino[0] - self.Char.Posicion[0]
        Seno = O / H
        Coseno = A / H
        Opuesto = Seno * 1 + self.Char.Posicion[1]
        
        Adj = Coseno * 1 + self.Char.Posicion[0]
        self.Destino = Opuesto, Adj"""

class HitBox(object):
    def __init__(self, (Left, Top), (Width, Height)):
        self.Bot = Top + Height
        self.Right = Left + Width
        self.Top = Top
        self.Left = Left
        self.TopLeft  = (self.Left , self.Top)
        self.TopRight = (self.Right, self.Top)
        self.BotRight = (self.Left , self.Bot)
        self.BotLeft  = (self.Right, self.Bot)
        self.Width = Width
        self.Height = Height
        
    def update(self, (Left, Top)):
        self.Bot = Top + self.Height
        self.Right = Left + self.Width
        self.Top = Top
        self.Left = Left
        self.TopLeft  = (self.Left , self.Top)
        self.TopRight = (self.Right, self.Top)
        self.BotRight = (self.Left , self.Bot)
        self.BotLeft  = (self.Right, self.Bot)   
        
    def containsPoint(self, (P_x,P_y)):
        return P_x >= self.Left and P_x <= self.Right and P_y >= self.Top and P_y <= self.Bot
    
    def collideHitBox(self, aHitBox):
        return any(map(aHitBox.containsPoint,  [self.TopLeft, self.TopRight, self.BotLeft, self.BotRight]))

