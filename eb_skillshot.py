import random, sys, pygame
from eb_render import *
LINE = 0 #voy a ver de reemplazarlos por constantes preexistentes en el main
SQR = 1
RED   =     (160, 25 ,  25 )

class skillshot():
    """Ataques"""
    efRate = 0 #rango de efectividad TOTAL (se divide por la cantidad de tiles)
    disRate = 0 #Cuantos tiles ocupa
    pattern = [] #En que forma se castea
    avPatterns = [] #Patterns disponibles
    pos = (0,0) #not that clear tbh, voy a ver de eliminarla
    locked = False #estado del skillshot, si locked significa que se ejecuta el pr?ximo turno.
    PlaceHolderColor = RED
    def __init__(self, efRate,disRate, avPatterns, Input, aChar):
        """inicializar dandole efRate, disRate y avPatterns"""
        self.efRate = efRate
        self.disRate = disRate
        self.avPatterns = avPatterns
        self.Input = Input
        self.mouse = Input.mouse()
        self.facing = Input.mouseDirection(aChar)

    def update(self, pattern):
        """pseudo-interfaz del skillshot, event handling"""
        prev = (0,0)

        if self.Input.Rotate():
            #si se toca L_ctrl se gira el skillshot
            self.rotate()

        if pattern == LINE:
            #Generar el pattern lineal
            for i in range(self.disRate):
                prev= tuple(map(sum, zip(prev, self.facing)))
                self.pattern.append(prev)

        if pattern == SQR:
            #Generar el pattern rectangular
            prev = self.mouse
            for i in range(self.disRate/2):
                prev = tuple(map(sum, zip(prev, self.facing)))
                self.pattern.append(prev)
            for double in self.pattern:
                if self.facing in (RIGHT, LEFT):
                    self.pattern.append(x,y+1)
                if self.facing in (UP, DOWN):
                    self.pattern.append(x+1,y)

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


