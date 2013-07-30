#! /usr/bin/env python
# Clase Mapa y Algoritmo Estrella
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

import math
from pygame import rect
from eb_render import Render

dClavesMapa = {'#':0,
               '0':1,
               'T':2,
               'S':3}

drClavesMapa = {v:k for k, v in dClavesMapa.iteritems()}

BOTRIGHT = 4
BOTLEFT = 3
TOPLEFT = 1
TOPRIGHT = 2

UP, RIGHT, DOWN, LEFT = (1,1), (1,-1), (-1,-1), (-1,1)
NE, SE, NO, SO = (0,-1), (1,0), (-1,0), (0,1)

dCollision = {NO:[TOPLEFT, TOPRIGHT, BOTLEFT, BOTRIGHT],
              NE:[TOPLEFT, TOPRIGHT, BOTLEFT, BOTRIGHT],
              SO:[TOPLEFT, TOPRIGHT, BOTLEFT, BOTRIGHT],
              SE:[TOPLEFT, TOPRIGHT, BOTLEFT, BOTRIGHT],
              RIGHT:[TOPLEFT, TOPRIGHT, BOTLEFT, BOTRIGHT],
              DOWN:[TOPLEFT, TOPRIGHT, BOTLEFT, BOTRIGHT],
              UP:[TOPLEFT, TOPRIGHT, BOTLEFT, BOTRIGHT],
              LEFT:[TOPLEFT, TOPRIGHT, BOTLEFT, BOTRIGHT]}

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
        
    def rectColission(self, ((left,top),(width,height)), comando):
        VerticesTile = [(left,top),(left+width, top),(left,top+height),(left+width, top+height)]
        
        
        for vertice in dCollision[comando]:
            x,y = VerticesTile[vertice-1]
            
            print x,y
        
            if comando[0] != 0:
                if x > int(x) and self.mapa[int(x)][int(y)] == 1:
                    return True
            
            if comando[1] != 0:
                if y > int(y) and self.mapa[int(x)][int(y)] == 1:
                    return True
        
        return False
       
        """if self.mapa[int(left)][int(top)] == 1:
           #if self.mapa[left][top] == 1:
           #     return False
           return True
           # print "TOPLEFT"
           # print "(",left, top,"),"
           # print "(",int(left), int(top),"),"

        if self.mapa[int(left)][int(top + height)] == 1:
            #print "BOTLEFT"
            #print "(",left,(top + height),")"
            #print "(",int(left), int(top + height), ")"
            #print  self.mapa[int(left)][int(top + height)]
            return True
        if self.mapa[int(left + width)][int(top)] == 1:
            #print "TOPRIGHT"
            #print "(",(left + width),top,")"
            #print "(",int(left + width),int(top),")"
            return True
        if self.mapa[int(left + width)][int(top + height)] == 1:
            #print "BOTRIGHT"
            #print "(",(left + width),(top + height),")"
            #print "(",int(left + width), int(top + height),")"
            return True
        return False"""
    

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




