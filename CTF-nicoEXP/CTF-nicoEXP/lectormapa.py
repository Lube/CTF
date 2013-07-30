#! /usr/bin/env python
# Clase Mapa y Algoritmo Estrella
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>

dClavesMapa = {'0':0,
               '#':1,
               'T':2,
               'S':3}

drClavesMapa = {v:k for k, v in dClavesMapa.iteritems()}

global pos_f

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

    def __str__(self):
        salida = ""
        for f in range(self.fil):
            for c in range(self.col):
                salida += drClavesMapa[self.mapa[f][c]]
            salida += "\n"
        return salida

class Board:
    height = 60
    width = 60


unMapa = Mapa('unmapa.txt')


