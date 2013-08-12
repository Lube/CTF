#! /usr/bin/env python
# Clase Mapa y Algoritmo Estrella
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

import math, string, socket, time
from pygame import rect
from eb_render import *

dClavesMapa = {'#':0,
               '0':1,
               'P':2,
               'R':3,
               'B':4}

drClavesMapa = {v:k for k, v in dClavesMapa.iteritems()}

VECS = [(0,1),(0,-1),(1,0),(-1,0)]
dVECS = {(0,1):'R', (0,-1):'L', (1,0):'B', (-1,0):'T'}
dWALLS = {'R'  :4 ,'L'  :2 ,'B'  :3 ,'T'   :1 ,
          'LT' :5 ,'RT' :7 ,'LB' :6 ,'RB'  :8 ,
          'LBT':12 ,'RLB':11,'RBT':10,'RLT' :9,
          'RL' :14,'BT' :13,''   :15,'RLBT':16}

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
    def __init__(self, archivo="unmapa.txt", data = None):
        if socket != None:
            self.mapa = leerMapa(archivo)
        else:
            self.mapa = string.split(data)
            
        self.fil = len(self.mapa)
        self.col = len(self.mapa[0])
        self.walls = []
        def getWalls(x,y):
            walls = ''
            
            for Dir in VECS:
                pX = x + Dir[0]
                pY = y + Dir[1]
                
                if pX < 0 or pX >= self.col or pY < 0  or pY >= self.fil:
                    pass
                else:
                    if self.mapa[pX][pY] == 1:
                        walls = walls + dVECS[Dir]
            return walls
        
        
        for i, columna in enumerate(self.mapa):
            self.walls.append([])
            for j, tile in enumerate(columna):
                self.walls[i].append(dWALLS[getWalls(i,j)])
            
        for i, columna in enumerate(self.walls):
            for j, tile in enumerate(columna):
                if self.mapa[i][j] == 1:
                    self.walls[i][j] = 15
    
    def enviar(self, aSocket):
        toSend = ''
        for line in range(self.fil):
            for char in range(self.col):
                toSend = toSend + str(self.mapa[line][char])
            toSend = toSend + '\n'
        print len(toSend)
        aSocket.sendall(toSend)
    
    
    def rectColission(self, ((left,top),(width,height   ))):
       
        if self.mapa[int(left)][int(top)] == 1:
           # print "TOPLEFT"
           # print "(",left, top,"),"
           # print "(",int(left), int(top),"),"
            return True
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
        return False
    
    def drawWall(self, render, FoB):
        for col in range(self.col):
            for fila in range(self.fil):
                if FoB == 'Back':
                    if self.walls[col][fila] in MAP_DIC_BP.keys():
                        render.drawWall(self.walls[col][fila], FoB, col, fila)
                else:
                    if self.walls[col][fila] in MAP_DIC_FP.keys():
                        render.drawWall(self.walls[col][fila], FoB, col, fila)
                    
    

    def draw(self, render, spritePiso, Chars, CharsEnemigos):
        N = self.col
        for p in range(0,N*2-1):
            for q in range(max(0, p-N+1), min(p, N-1)):
                col = q
                fila = p - q - 1
                if self.walls[fila][col] in MAP_D_BP_KEYS: #DIBUJA PAREDES TRASERAS
                        render.drawWall(self.walls[fila][col], 'Back', fila, col)
                if self.mapa[fila][col] == 0: #DIBUJA PISOS
                    render.drawSprite(spritePiso, fila, col)
                else:
                    render.drawPlaceHolder(WHITE, fila, col)
                
                for Char in Chars:
                    x = ((((Char.Posicion[0] * 2) // 1) + 1) // 2)
                    y = ((((Char.Posicion[1] * 2) // 1) + 1) // 2)
                    if x == fila and y == col:
                        Char.draw(render)
                        if self.walls[fila-1][col] in MAP_D_FP_KEYS: #DIBUJA PAREDES DELANTERAS
                            render.drawWall(self.walls[fila-1][col], 'Front', fila-1, col)
                        if self.walls[fila+1][col-1] in MAP_D_FP_KEYS: #DIBUJA PAREDES DELANTERAS
                            render.drawWall(self.walls[fila+1][col-1], 'Front', fila+1, col-1)
                        if self.walls[fila][col-1] in MAP_D_FP_KEYS: #DIBUJA PAREDES DELANTERAS
                            render.drawWall(self.walls[fila][col-1], 'Front', fila, col-1)
                        #if self.walls[fila][col+1] in MAP_DIC_FP.keys(): #DIBUJA PAREDES DELANTERAS
                        #    render.drawWall(self.walls[fila][col], 'Front', fila, col+1)
                for Char in CharsEnemigos:
                    x = ((((Char.Posicion[0] * 2) // 1) + 1) // 2)
                    y = ((((Char.Posicion[1] * 2) // 1) + 1) // 2)
                    if x == fila and y == col:
                        Char.draw(render)
                    
                if self.walls[fila][col] in MAP_D_FP_KEYS: #DIBUJA PAREDES DELANTERAS
                        render.drawWall(self.walls[fila][col], 'Front', fila, col)

    def __str__(self):
        salida = ""
        for f in range(self.fil):
            for c in range(self.col):
                salida += drClavesMapa[self.mapa[f][c]]
            salida += "\n"
        return salida




