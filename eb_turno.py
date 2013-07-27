#! /usr/bin/env python
# Clase Turno, Action, Movimiento, AutoAtaque
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

from eb_lectormapa import Mapa

class Action():
    pass

class Walk(Action):
    def __init__(self, Pos):
        self.Pos = Pos

    def play(self, aChar):
        aChar.Posicion = self.Pos



class Run(Action):
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





