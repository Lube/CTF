#! /usr/bin/env python
# Clase Personaje
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

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
COST_SKILL = 50
WALK_ESC = 0.2
RUN_ESC = 0.3
FASE_P = 'planeamiento'
FASE_A = 'accion'

#           R,    G,    B
BLACK =     (0  , 0  ,  0  )
WHITE =     (255, 255,  255)
GREEN =     (0  , 160,  50 )
RED   =     (160, 25 ,  25 )

from eb_render import Render
from eb_turno import *
from eb_lectormapa import Mapa
from eb_skillshot import *

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

class Personaje:
    #AtkSpeed
    #MovSpeed
    #Sprite
    #Posicion
    Estado    = STATE_WALK
    PlaceHolderColor = GREEN
    acSkill = None


    def __init__(self, AtkSpeed = 10, MovSpeed = 10, Posicion = (5,5)):
            self.AtkSpeed = AtkSpeed
            self.MovSpeed = MovSpeed
            self.Posicion = Posicion

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

        if anInput.nSkill != 0:
            self.skill(nSkill, anInput)



    def canMove(self, mapa, comando):
        if (self.Estado == STATE_STUN) or (self.Estado == STATE_FEAR):
            return False, NONE
        elif self.Estado == STATE_RUN:
            if mapa.pos(self.Posicion |x| (RUN_ESC |y| comando)):
                return True
            else:
                return False
        else:
            if mapa.pos(self.Posicion |x| (WALK_ESC |y| comando)):
                return True
            else:
                return False

    def wait(self):
        addAction(self.Turno, Wait, self.Posicion)
        self.ActionPoints -= COST_WAIT


    def walk(self, comando):
        if not self.Turno or not sameLastAction(self.Turno, Walk):
            addAction(self.Turno, Walk, self.Posicion)

        self.Posicion = self.Posicion |x| (WALK_ESC |y| comando)
        self.ActionPoints -= COST_WALK

        addAction(self.Turno, Walk, self.Posicion)


    def run(self, comando):
        if not self.Turno or not sameLastAction(self.Turno, Run):
            addAction(self.Turno, Run, self.Posicion)

        self.Posicion = self.Posicion |x| (RUN_ESC |y| comando)
        self.ActionPoints -= COST_RUN

        addAction(self.Turno, Run, self.Posicion)

    def skill(self, nSkill, Input):
        selectedSkill = avSkills[nSkill]
        self.ActionPoints -= COST_SKILL
        self.acSkill = selectedSkill(Input, self)
        while not self.acSkill.locked:
            self.acSkill.update(self.acSkill.avPatterns[0])
        addAction(self.Turno, selectedSkill, (Input, aChar))
        self.acSkill = None

    def draw(self, render):
        render.drawPlaceHolder(self.PlaceHolderColor, self.Posicion[0], self.Posicion[1])
        if self.acSkill != None:
            for tile in acSkill.pattern:
                 render.drawPlaceHolder(self.PlaceHolderColor, tile[0], tile[1])



def addAction(aTurno, Clase, Args = None):
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

    Fase = FASE_P
    ActionPoints = 100


    def __init__(self, Posicion = (5,5)):
            self.Posicion = Posicion
            self.Turno = []


    def Play(self, PlayAction):
        PlayAction.play(self)
        self.Turno.remove(PlayAction)
