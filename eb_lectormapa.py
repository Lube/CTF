#! /usr/bin/env python
# Clase Mapa y Algoritmo Estrella
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

import math
from eb_render import Render

dClavesMapa = {'#':0,
               '0':1,
               'T':2,
               'S':3}

drClavesMapa = {v:k for k, v in dClavesMapa.iteritems()}

#           R,    G,    B
BLACK =     (0  , 0  ,  0  )
WHITE =     (255, 255,  255)
GREEN =     (0  , 160,  50 )


# Lee un archivo de texto y lo convierte en una lista.
def leerMapa(archivo):
    vMap = []
    mapa = open(archivo, "r")
    mapa = mapa.readlines()

    for i, line in enumerate(mapa):
        mapa[i] = line.rstrip('\n')

    for i, line in enumerate(mapa):
        vMap.append([])
        for j, clave in enumerate(line):
            if mapa[i][j] != ' ':
                vMap[i].append(dClavesMapa[mapa[i][j]])
    return vMap

class Mapa:
    def __init__(self, archivo="unmapa.txt"):
        self.mapa = leerMapa(archivo)
        self.fil = len(self.mapa)
        self.col = len(self.mapa[0])
        
    def pos(self, (PosX, PosY)):
        if self.mapa[math.trunc(PosX)][math.trunc(PosY)] == 0:
            return True
        return False
    

    def draw(self, render):
        for col in range(self.col):
            for fila in range(self.fil):
                if self.mapa[fila][col] == 0:
                    aColor = BLACK
                else:
                    aColor = WHITE
                render.drawPlaceHolder(aColor, fila, col)

    def __str__(self):
        salida = ""
        for f in range(self.fil):
            for c in range(self.col):
                salida += drClavesMapa[self.mapa[f][c]]
            salida += "\n"
        return salida




