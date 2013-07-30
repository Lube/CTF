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
    
    def __init__(self, Origen, Destino):
        self.Origen = Origen
        self.Destino = Destino
        self.Pos = Origen
        self.Step = 0
        self.vTrayectoria = self.Destino[0] - self.Origen[0], self.Destino[1] - self.Origen[1]
        self.Over = False
        
        Mag = math.sqrt(sum([self.vTrayectoria[i] ** 2 for i in [0,1]]))
        self.vTrayectoria = [self.vTrayectoria[i]/Mag for i in [0,1]]
        
    def play(self):
        self.Step += 1
        X = self.vTrayectoria[0]
        Y = self.vTrayectoria[1]
                    
        #X, Y = X, Y
        self.Pos = self.Pos |x| (X,Y)
        
        if self.Step >= self.Range:
            self.Over = True
        
        
        
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

    def play(self, aChar):
        aChar.Posicion = self.Pos



class Run(Action):
    Persistent = False
    def __init__(self, Pos):
        self.Pos = Pos

    def play(self, aChar):
        aChar.Posicion = self.Pos


class Wait(Action):
    Persistent = False
    Pos = (0,0)
    def __init__(self, Pos):
        self.Pos = Pos

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
