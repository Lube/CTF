#! /usr/bin/env python
# Clase Personaje
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>


RIGHT, UP, LEFT, DOWN = (1,1), (1,-1), (-1,-1), (-1,1)
NE, SE, NO, SO = (0,-1), (1,0), (-1,0), (0,1)

LINE = 0
SQR = 1
ATK_SPEED_DPS = 12
MOV_SPEED_DPS = 8
DAMAGE_DPS = 8
HITPOINTS_DPS = 100
STATE_WALK = 'walk'
STATE_FEAR = 'fear'
STATE_STUN = 'stun'
STATE_RUN = 'run'
COST_RUN = 8
COST_WALK = 5
COST_WAIT = 10
COST_SKILLS = [50,50,50,50]
WALK_ESC = 0.2
RUN_ESC = 0.3
FASE_P = 'planeamiento'
FASE_A = 'accion'


#           R,    G,    B
BLACK =     (0  , 0  ,  0  )
WHITE =     (255, 255,  255)
GREEN =     (0  , 160,  50 )
RED   =     (160, 25 ,  25 )

import pygame, math
from eb_render import Render
from eb_turno import *
from eb_lectormapa import Mapa


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





#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#





class skillshot():
    """Ataques"""
    efRate = 0 #rango de efectividad TOTAL (se divide por la cantidad de tiles)
    disRate = 0 #Cuantos tiles ocupa
    Pattern = [] #En que forma se castea
    avPatterns = [] #Patterns disponibles
    locked = False #estado del skillshot, si locked significa que se ejecuta el pr?ximo turno.
    PlaceHolderColor = RED
    def __init__(self, Input, aChar):
        """inicializar dandole efRate, disRate y avPatterns"""
        self.Input = Input
        self.mouse = Input.mouse()
        self.char = aChar
        self.facing = Input.mouseDirection(self.char)

        
    def update(self, pattern):
        self.Pattern = []
        if self.mouse == (None, None):
            self.mouse = (0,0)
        """pseudo-interfaz del skillshot, event handling"""
        prev = (0,0)
        self.facing = self.Input.mouseDirection(self.char)
        if self.Input.Rotate:
            #si se toca L_ctrl se gira el skillshot
            self.rotate()

        if pattern == LINE:
            #Generar el pattern lineal
            for i in range(self.disRate):
                prev= tuple(map(sum, zip(prev, self.facing)))
                self.Pattern.append(prev)

        if pattern == SQR:
            #Generar el pattern rectangular
            """prev = self.Input.mouse()
            for i in range(self.disRate/2):
                prev = prev |x| self.facing
                self.Pattern.append(prev)
               # print self.Pattern
            acPattern = self.Pattern
            for q,y in acPattern:
                if self.facing in (RIGHT, LEFT):
                    self.Pattern.append((q,y+1))
                if self.facing in (UP, DOWN"""
            self.Pattern.append(self.Input.mouse())

        if self.Input.Click:
            #Si clickea se confirma el movimiento
            self.locked = True
       


    def rotate(self):
        """rotar """
        if self.facing == RIGHT:
            self.facing = DOWN
        if self.facing == DOWN:
            self.facing = LEFT
        if self.facing == LEFT:
            self.facing = UP
        if self.facing == UP:
            self.facing = RIGHT

    def draw(self, render):
        for tile in self.pattern:
            render.drawPlaceHolder(self.PlaceHolderColor, tile[0], tile[1])


class Ray(skillshot):
    efRate = 100
    disRate = 4
    avPatterns = [LINE]
    pattern = LINE

    def play(self):
        self.update(pattern, Input)

class Blast(skillshot):
    efRate = 100
    disRate = 6
    avPatterns = [SQR]

    def play(self, aChar):
        self.update(pattern, Input)



#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#



class Personaje:
    #AtkSpeed
    #MovSpeed
    #Sprite
    #Posicion
    Estado    = STATE_WALK
    PlaceHolderColor = GREEN
    Habilidades = []


    def __init__(self, AtkSpeed = 10, MovSpeed = 10, Posicion = (5,5)):
            self.AtkSpeed = AtkSpeed
            self.MovSpeed = MovSpeed
            self.Posicion = Posicion
            self.acSkill  = None

    def getPlayAction(self):
        if self.Turno:
            PlayAction = self.Turno[0]
            return PlayAction
        else:
            return None

    def cambiaEstado(self):
        if self.Estado == STATE_WALK:
            self.Estado = STATE_RUN
        else:
            self.Estado = STATE_WALK

    def cambiaFase(self):
        if self.Fase == FASE_P:
            self.Fase = FASE_A
            self.PlaceHolderColor = RED
        else:
            self.Fase = FASE_P
            self.ActionPoints = 100
            self.PlaceHolderColor = GREEN

    def update(self, anInput, unMapa):
        if self.ActionPoints <= 0 or anInput.ChangeSignal:
                self.cambiaFase()

        if anInput.WalkRun:
            self.cambiaEstado()

        if anInput.Order != (0,0):
            if self.canMove(unMapa, anInput.Order):
                if self.Estado == STATE_WALK:
                    self.walk(anInput.Order)
                elif self.Estado == STATE_RUN:
                    self.run(anInput.Order)

        if anInput.Wait:
            self.wait()

        if anInput.nSkill != None:
            self.skill(anInput.nSkill, anInput)

                    




    def canMove(self, mapa, comando):
        if (self.Estado == STATE_STUN) or (self.Estado == STATE_FEAR):
            return False
        elif self.Estado == STATE_RUN:
            Escalar = RUN_ESC
        else:
            Escalar = WALK_ESC

        R =((self.Posicion |x| (Escalar |y| comando)),(0.5,0.5))

        if mapa.rectColission(R):
            return False
        return True

    def wait(self):
        addAction(self.Turno, Wait, self.Posicion)
        self.ActionPoints -= COST_WAIT


    def walk(self, comando):
        if not self.Turno or not sameLastAction(self.Turno, Walk):
            addAction(self.Turno, Walk, self.Posicion)

        self.Posicion = self.Posicion |x| (WALK_ESC |y| comando)
        self.Posicion = round(self.Posicion[0], 1), round(self.Posicion[1], 1)
        self.ActionPoints -= COST_WALK

        addAction(self.Turno, Walk, self.Posicion)


    def run(self, comando):
        if not self.Turno or not sameLastAction(self.Turno, Run):
            addAction(self.Turno, Run, self.Posicion)

        self.Posicion = self.Posicion |x| (RUN_ESC |y| comando)
        round(self.Posicion[0], 1)
        round(self.Posicion[1], 1)
        self.ActionPoints -= COST_RUN

        addAction(self.Turno, Run, self.Posicion)

    def skill(self, nSkill, Input):
        selectedSkill = self.avSkills[nSkill]
        self.ActionPoints -= COST_SKILLS[nSkill]
        self.acSkill = selectedSkill(Input, self)


    def draw(self, render):
        render.drawPlaceHolder(self.PlaceHolderColor, self.Posicion[0], self.Posicion[1], 0, 'personaje')


def addAction(aTurno, Clase, Args):
        aTurno.append(Clase(Args))

def sameLastAction(aTurno, aClass):
        return aTurno[-1].__class__.__name__ == aClass.__name__

def sameFirstAction(aTurno, aClass):
        return aTurno[0].__class__.__name__ == aClass.__name__


class DPS(Personaje):
    AtkSpeed = ATK_SPEED_DPS
    MovSpeed = MOV_SPEED_DPS
    Damage   = DAMAGE_DPS
    HitPoints = HITPOINTS_DPS
    avSkills = [Ray, Blast]
    acSkill = None
    Fase = FASE_P
    ActionPoints = 100


    def __init__(self, Posicion = (5,5)):
            self.Posicion = Posicion
            self.Turno = []


    def Play(self, PlayAction):
        PlayAction.play(self)
        self.Turno.remove(PlayAction)
        
        
        
