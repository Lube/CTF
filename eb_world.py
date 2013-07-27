import pygame, random, sys, time, math, os, copy

from eb_lectormapa import *
from eb_turno import *
from eb_char import *
from eb_input import *
from eb_camera import *
from eb_render import *
from eb_skillshot import *
from pygame.locals import *

RIGHT, UP, LEFT, DOWN = (1,1), (1,-1), (-1,-1), (-1,1)
NE, SE, NO, SO = (0,-1), (1,0), (-1,0), (0,1)

dFACINGS = {RIGHT:0, DOWN:1, NE:6, NO:3 ,UP:4 ,SE:5 ,SO:2 ,LEFT:7}

FPS = 30

WINDOWWIDTH, WINDOWHEIGHT = 800, 600
TILEH, TILEW, GAPSIZE = 32, 64, 1
BOARDWIDTH = 15
HALF = WINDOWWIDTH / 2
HTILEH = 0.5 * TILEH
HTILEW = 0.5 * TILEW

#           R,    G,    B
BLACK =     (0  , 0  ,  0  )
WHITE =     (255, 255,  255)
GREEN =     (0  , 160,  50 )


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, Input
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('CTF v0.1')
    #--------------------------
    BASICFONT = pygame.font.Font('freesansbold.ttf', 36)
    unMapa = Mapa('unMapa.txt')
    SkToUse = []
    Chars = []
    Chars.append(DPS((7,6)))
    Chars.append(DPS((3,3)))
    CharSelected = Chars[0]
    Input = Input()
    aCamera = Camera('STATIC', (0,0))
    aRender = Render(aCamera, DISPLAYSURF)
    #--------------------------
    while not Input.Quit:
        DISPLAYSURF.fill((0,0,0))
        unMapa.draw(aRender)

        for char in Chars:
            char.draw(aRender)
        Input.update()

        if Input.CameraOrder != None:
            aCamera.update(aCamera.xyTile |x| Input.CameraOrder)

        if CharSelected.Fase == FASE_A:
            CharSelected = Chars[(Chars.index(CharSelected)+ 1) % len(Chars)]

        if CharSelected.Fase == FASE_P:
            CharSelected.update(Input, unMapa)

        if all(map(lambda x: x.Fase == FASE_A, Chars)):
            if all(map(lambda x: not x.Turno, Chars)):
                for Char in Chars:
                    Char.cambiaFase()
            for Char in Chars:
                if Char.Turno:
                    Char.Play(Char.getPlayAction())


        pygame.display.update()
        FPSCLOCK.tick(FPS)


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

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


if __name__ == '__main__':
    main()
