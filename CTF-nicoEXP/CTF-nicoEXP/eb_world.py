import pygame, random, sys, time, math, os, copy, socket

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

FPS = 12

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



def main(SoC, IP):
    global FPSCLOCK, DISPLAYSURF, BASICFONT, Input
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('CTF v0.1')
    #--------------------------
    BASICFONT = pygame.font.Font('freesansbold.ttf', 36)
    unMapa = Mapa('unMapa.txt')
    ActiveActions = []
    Chars = []
    Chars.append(DPS((7,6)))
    Chars.append(DPS((3,3)))
    CharSelected = Chars[0]
    Input = Input()
    aCamera = Camera('STATIC', (0,0))
    aRender = Render(aCamera, DISPLAYSURF)
    #--------------------------
    if SoC != None:
        # Create a TCP/IP socket
        unSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = ('localhost', 10000)
        print "1"
        if SoC == 'server':
            unSocket.bind(server_address)
            unSocket.listen(1)
            print "2"
            # Wait for a connection
            connection, client_address = unSocket.accept()
            try:
            # Receive the data in small chunks and retransmit it
                while True:
                        data = connection.recv(16)
                        print >>sys.stderr, 'received "%s"' % data
                        if data:
                            connection.sendall(data)
                        else:
                            break
                        data = []
            finally:
                # Clean up the connection
                connection.close()
        if SoC == 'cliente':
            print "3"
            unSocket.connect(server_address)
            try:
                # Send data
                unSocket.sendall("hola mundo")
                # Look for the response
                amount_received = 0
                amount_expected = len("hola mundo")
    
                while amount_received < amount_expected:
                    data = unSocket.recv(16)
                    amount_received += len(data)
            finally:
                unSocket.close()
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
            CharSelected.update(Input, unMapa, aCamera)
            if CharSelected.acSkill != None:
                CharSelected.acSkill.draw(aRender, 'planning')
                #OrigenSk, FinSk = CharSelected.SketchAcSkill
                #pygame.draw.line(DISPLAYSURF, RED, Tiles2Coords(OrigenSk)|x|(-aCamera.x, -aCamera.y+8), Tiles2Coords(FinSk), 6)
                #aCamera.block()
                
            

        if all(map(lambda x: x.Fase == FASE_A, Chars)):
            if all(map(lambda x: not x.Turno, Chars)):
                for Char in Chars:
                    Char.cambiaFase()
            for Char in Chars:
                if Char.Turno:
                    Action = Char.getPlayAction()
                    if Action.Persistent:
                        ActiveActions.append(Action)
                        Char.Turno.remove(Action)
                    else:
                        Char.Play(Action)

        
        for anAction in ActiveActions:
                anAction.play()
                anAction.draw(aRender)
                if anAction.Over:
                    ActiveActions.remove(anAction)
        
        
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
        "Loads a s2trip of images and returns them as a list"
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
    main(sys.argv[1], sys.argv[2])


