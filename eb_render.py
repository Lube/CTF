#! /usr/bin/env python
# Clase Render
# Copyright (C) 2012  EGGBREAKER <eggbreaker@live.com.ar>
import pygame

from pygame.locals import *



WINDOWWIDTH, WINDOWHEIGHT = 500, 300
TILEH, TILEW = 48, 96
HALF = WINDOWWIDTH / 2
HTILEH = 0.5 * TILEH
HTILEW = 0.5 * TILEW

PHEIGHT = 24 
PHHEIGHT = 12 
PHWIDTH = 24

MAP_DIC_NP = {15:''}
MAP_DIC_BP = {1:'L',2:'T',5:'LT',6:'T',7:'L',9:'LT',10:'L',11:'T',12:'LT',13:'L',14:'T'}
MAP_DIC_FP = {3:'R',4:'B',6:'R',7:'B',8:'RB',9:'B',10:'RB',11:'RB',12:'R',13:'R',14:'B'}

MAP_D_FP_KEYS = MAP_DIC_FP.keys()
MAP_D_BP_KEYS = MAP_DIC_BP.keys()

WHITE = (255,255,255)
BLUE = (0,0,120)
BLACK = (0,0,0)

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


class Render():

    def __init__(self, aCamera, aSurface):
        self.Camera = aCamera
        self.Surface = aSurface
        
    def drawLine(self, color, Origen, Destino, aCamera = 0):
        if aCamera == 0:
            aCamera = self.Camera
        O = Tiles2Coords(Origen) |x| (-aCamera.x, -aCamera.y)
        D = Tiles2Coords(Destino)|x| (-aCamera.x, -aCamera.y)
        
        pygame.draw.line(self.Surface, color, O, D, 6)
    

    def drawPlaceHolder(self, color, Col, Fila, aCamera = 0, source = 'terreno'):
        if aCamera == 0:
            aCamera = self.Camera

        X, Y = Tiles2Coords((Col, Fila))
        X, Y = X-aCamera.x, Y-aCamera.y
        if (X<aCamera.xRange and X>-100 and Y>-100 and Y<aCamera.yRange):
            if source == 'terreno':
                pygame.draw.polygon(self.Surface, color, [(X,Y),(X+HTILEW,Y+HTILEH),(X,Y+TILEH),(X-HTILEW, Y+HTILEH)])
            else:
                pygame.draw.polygon(self.Surface, color, [(X,Y),(X+PHWIDTH,Y+PHHEIGHT),(X,Y+PHEIGHT),(X-PHWIDTH, Y+PHHEIGHT)])
        
    def drawWall(self, Code, FoB, Col, Fila, aCamera = 0):
        if aCamera == 0:
            aCamera = self.Camera
        D = None
        X, Y = Tiles2Coords((Col, Fila))
        X, Y = X-aCamera.x, Y-aCamera.y
        
        if FoB == 'Back':
            D = MAP_DIC_BP
        else:
            D = MAP_DIC_FP
        for key in D[Code]:
            if key == 'L':
                pygame.draw.polygon(self.Surface, BLUE, [(X,Y),(X-HTILEW,Y+HTILEH),(X-HTILEW,Y),(X, Y-HTILEH)])
            if key == 'R':
                pygame.draw.polygon(self.Surface, BLACK, [(X+HTILEW,Y+HTILEH),(X,Y+TILEH),(X,Y+HTILEH),(X+HTILEW, Y)])
            if key == 'T':
                pygame.draw.polygon(self.Surface, BLUE, [(X,Y),(X+HTILEW,Y+HTILEH),(X+HTILEW,Y),(X, Y-HTILEH)])
            if key == 'B':
                pygame.draw.polygon(self.Surface, BLACK, [(X-HTILEW,Y+HTILEH),(X,Y+TILEH),(X,Y+HTILEH),(X-HTILEW, Y)])
        

    def drawSprite(self, sprite, Col, Fila, aCamera = 0):
        if aCamera == 0:
            aCamera = self.Camera
        
        X, Y = Tiles2Coords((Col, Fila))
        X, Y = X-aCamera.x, Y-aCamera.y
        if (X<aCamera.xRange and X>-100 and Y>-100 and Y<aCamera.yRange):
            self.Surface.blit(sprite, (X-HTILEW,Y))

class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image, rect
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

def Tiles2Coords((Col, Fila)):
    Y = (Col + Fila) * HTILEH 
    X = HALF + (Col*HTILEW) - (Fila*HTILEW)
    
    return X,Y

