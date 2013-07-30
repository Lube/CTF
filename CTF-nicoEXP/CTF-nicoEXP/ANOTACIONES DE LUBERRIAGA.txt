import pygame, random, sys, time, math, os, copy

from eb_lectormapa import *
from eb_turno import *
from eb_char import *
from eb_input import *
from eb_camera import *
from eb_render import *

from pygame.locals import *

RIGHT, UP, LEFT, DOWN = (1,1), (1,-1), (-1,-1), (-1,1)
NE, SE, NO, SO = (0,-1), (1,0), (-1,0), (0,1)

dFACINGS = {RIGHT:0, DOWN:1, NE:6, NO:3 ,UP:4 ,SE:5 ,SO:2 ,LEFT:7}

#NONE = (0,0)
FPS = 30

WINDOWWIDTH, WINDOWHEIGHT = 600, 400
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

    global FPSCLOCK, DISPLAYSURF, BASICFONT, Input#aSpriteSheet, unMapa, aCamera, tileList, Commands, aChar, command, Collisionables

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('CTF v0.1')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 36)

    #NR = True
    #print NR
    #mainWorld = level(True)

    unMapa = Mapa('unMapa.txt')

    #aSpriteSheet = spritesheet(unMapa.tileset)
    #bSpriteSheet = spritesheet('swordwalking.png')
    Chars = []
    Chars.append(DPS((1,1)))
    Chars.append(DPS((3,3)))
    CharSelected = Chars[0]
    #for directions in range(8):
    #        aChar.animations.append(bSpriteSheet.load_strip((0,directions*48,48,48), 8, colorkey=(0, 0, 0)))

    #tileList = {}

    #command = (0,0)
    Input = Input()
    aCamera = Camera('STATIC', (0,0))
    aRender = Render(aCamera, DISPLAYSURF)
    #Collisionables = unMapa.getCollisionables()
    
    
    
    while not Input.Quit:
        
        #aCamera.update(CharSelected.Posicion)
        #print aChar.pos
        DISPLAYSURF.fill((0,0,0))
        unMapa.draw(aRender)
        for char in Chars:
            char.draw(aRender)
        #CharA.draw(aRender)
        #CharB.draw(aRender)
        
        Input.update()
        
        #CharSelected.update()
        
        if CharSelected.Fase == FASE_A:
            CharSelected = Chars[(Chars.index(CharSelected)+ 1) % len(Chars)]
                
        if CharSelected.Fase == FASE_P:
            CharSelected.update(Input, unMapa)
        
            
        
        """if Input.ChangeSignal and CharSelected.Fase == FASE_P:
            CharSelected.cambiaFase()
            CharSelected = Chars[(Chars.index(CharSelected)+ 1) % len(Chars)]
            
        if Input.WalkRun and CharSelected.Fase == FASE_P:
            CharSelected.cambiaEstado()
        
        if CharSelected.Fase == FASE_P:
            CharSelected.move(Input.Order)"""
        
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



"""def readMap(filename):
    assert os.path.exists(filename), 'No se puede encontrar el archivo'
    mapFile = open(filename, 'r')
    # Cada nivel finaliza con una nueva linea
    lineas = mapFile.readlines() + ['\r\n']
    mapFile.close() # Cerramos el Archivo

    mapObj = mapObject() # Objeto mapa

    readingLayer, readingData = False, False
    currentLayer = ''
    nRows = -1
    csv = []

    for nLinea in lineas:
        # Process each line that was in the level file.
        line = nLinea.rstrip('\r\n')

        if ';' in line:
            # Ignore the ; lines, they're comments in the level file.
            line = line[:line.find(';')]
        if line.startswith('width='):
            mapObj.width = int(line[line.find('width='):].lstrip('width='))
        if line.startswith('height='):
            mapObj.height = int(line[line.find('height='):].lstrip('height='))
        if line.startswith('tilewidth='):
            mapObj.tilew = int(line[line.find('tilewidth='):].lstrip('tilewidth='))
        if line.startswith('tileheight='):
            mapObj.tileh = int(line[line.find('tileheight='):].lstrip('tileheight='))
        if 'tileset=' in line:
            tilesetdata = line[line.find('tileset='):].lstrip('tileset=').split(',')
            mapObj.tileset = tilesetdata[0]
            mapObj.tilesetXOffset = int(tilesetdata[3])
            mapObj.tilesetYOffset = int(tilesetdata[4])
            mapObj.tilesetWidth = int(tilesetdata[5])
            mapObj.tilesetHeight = int(tilesetdata[6])

        if '[layer]' in line:
            readingLayer = True

        if readingLayer and line == '':
            readingLayer = False
            readingData = False

        if 'type=' in line and readingLayer:
            currentLayer = line[line.find('type='):].lstrip('type=')
            mapObj.layers[currentLayer] = []
            nRows = 0
            #mapObj.layers[nLayers][0] = line[line.find('type='):].lstrip('type=')

        if 'data=' in line:
            readingData = True

        if readingLayer and readingData and 'data=' not in line:
            mapObj.layers[currentLayer].append([])
            csv = line.rstrip(',').split(',')
            for id in csv:
                trueId = int(id)
                if currentLayer == 'object':
                    z, trueId = trueId % 10, trueId // 10
                x = ((trueId-1) % (mapObj.tilesetWidth / mapObj.tilew)) * mapObj.tilew
                y = int((trueId-1) / (mapObj.tilesetWidth / mapObj.tilew)) * mapObj.tileh
                if currentLayer == 'object':
                    mapObj.layers[currentLayer][nRows].append((x,y,z))
                    print (x,y,z)
                mapObj.layers[currentLayer][nRows].append((x,y))
            nRows += 1

    return mapObj"""

"""class mapObject:
    width = 0
    height = 0
    tilew = 0
    tileh = 0
    tileset = ''
    tilesetXOffset = 0
    tilesetYOffset = 0
    tilesetWidth = 0
    tilesetHeight = 0
    layers = {}

    def getCollisionables(self):
        Collisionables = []
        for y, rows in enumerate(self.layers['collision']):
            for x, tile in enumerate(rows):
                    if tile != (960, -32):
                        Collisionables.append(pygame.Rect(x-1, y-1,1,1))
        return Collisionables

    def draw(self, aCamera, aLayer):
            if aLayer == 'object':
                for x, rows in filter((lambda (x,y): x < aCamera.xyTile[1] + aCamera.yRange and x > aCamera.xyTile[1] - aCamera.yRange), enumerate(self.layers[aLayer])):
                    for y, tile in filter(lambda (x,y): x < aCamera.xyTile[0] + aCamera.xRange and x > aCamera.xyTile[0] - aCamera.xRange, enumerate(rows)):
                        if tile in tileList:
                            drawtile(tileList[tile][0], y+tile[2], x)
                        else:
                            tileList[tile] =  aSpriteSheet.image_at((tile[0],tile[1],64,32), colorkey=(0, 0, 0))
                            drawtile(tileList[tile][0], y+tile[2], x)

            else:
                for x, rows in filter((lambda (x,y): x < aCamera.xyTile[1] + aCamera.yRange and x > aCamera.xyTile[1] - aCamera.yRange), enumerate(self.layers[aLayer])):
                    for y, tile in filter(lambda (x,y): x < aCamera.xyTile[0] + aCamera.xRange and x > aCamera.xyTile[0] - aCamera.xRange, enumerate(rows)):
                            if tile in tileList:
                                drawtile(tileList[tile][0], y, x)
                            else:
                                tileList[tile] =  aSpriteSheet.image_at((tile[0],tile[1],64,32), colorkey=(0, 0, 0))
                                drawtile(tileList[tile][0], y, x)

class character:
    animations = []
    facing = RIGHT
    pos = [10,10]
    state = 3
    moving = False

    def draw(self):
        drawtile(self.animations[FACINGS[self.facing]][self.state][0], self.pos[0], self.pos[1])

    def update(self, command, collisionables):
        if command == (0,0) or self.willCollision(collisionables):
            if command != (0,0):
                self.facing = command
            self.moving = False
            self.state = 3
        else:
            self.facing = command
            xVec, yVec = command
            self.moving = True
            self.state = (self.state + 1) % len(self.animations[FACINGS[self.facing]])
            X,Y = self.pos
            self.pos = (X + xVec *0.1, Y-yVec * 0.1)


    def willCollision (self, collisionables):
        playerA = (self.pos[0] + (self.facing[0]*0.1))+0.5, (self.pos[1] - (self.facing[1]*0.1))+0.5
        playerB = (self.pos[0] + (self.facing[0]*0.1))-0.5, (self.pos[1] - (self.facing[1]*0.1))-0.2
        playerC = (self.pos[0] + (self.facing[0]*0.1))+0.2, (self.pos[1] - (self.facing[1]*0.1))-0.2
        playerD = (self.pos[0] + (self.facing[0]*0.1))-0.5, (self.pos[1] - (self.facing[1]*0.1))+0.5

        for tile in collisionables:
            if  tile.collidepoint(playerA) or tile.collidepoint(playerB)or tile.collidepoint(playerC)or tile.collidepoint(playerD):
                return True
        return False"""


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

"""class level():
    room = 'start'
    playable = False
    background = (0,0,0)

    def __init__(self,playable):
        self.playable = playable



    def update(self, NR):
        if self.room == 'start':
            self.start()
        if self.room == 'world':
            self.world(NR)"""

if __name__ == '__main__':
    main()
