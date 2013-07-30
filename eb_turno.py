#! /usr/bin/env python
# Clase Turno, Action, Movimiento, AutoAtaque
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

from eb_lectormapa import Mapa

#class ActionFactory(object):

class Action():
    #Target = None
    pass

class Walk(Action):
 #   MovList = []
    def __init__(self, Pos):
        self.Pos = Pos
    
    def play(self, aChar):
        aChar.Posicion = self.Pos
        

        
class Run(Action):
#    MovList = []

    def __init__(self, Pos):
        self.Pos = Pos
        
    def play(self, aChar):
        aChar.Posicion = self.Pos


class Wait(Action):
    Pos = (0,0)
    
    def __init__(self, Pos):
        self.Pos = Pos
    
    def play(self, aChar):
        aChar.Posicion = self.Pos


class AutoAtaque(Action):

    def __init__(self, Char, Target, Forced = False):
        self.Target = Target
        self.Forced = Forced





