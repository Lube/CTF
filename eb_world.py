import pygame, random, sys, time, math, os, copy, socket, select

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
SIZE_TEAM = 2
WINDOWWIDTH, WINDOWHEIGHT = 500, 300
TILEH, TILEW = 48, 96
BOARDWIDTH = 15
HALF = WINDOWWIDTH / 2
HTILEH = 0.5 * TILEH
HTILEW = 0.5 * TILEW

#           R,    G,    B
BLACK =     (0  , 0  ,  0  )
WHITE =     (255, 255,  255)
GREEN =     (0  , 160,  50 )

LISTENPORT = 10000



def main(SoC, IP):
    global FPSCLOCK, DISPLAYSURF, BASICFONT, Input
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('CTF v0.1')
    #--------------------------
    BASICFONT = pygame.font.Font('freesansbold.ttf', 36)
    MessageSent = False
    MessageReceived = False
    toSend = ''
    data = ''
    ActiveActions = []
    ActiveActionsEnemigas = []
    Chars = []
    CharsEnemigos = []
    Chars.append(DPS((12,12)))
    Chars.append(DPS((14,14)))
    CharSelected = Chars[0]
    Input = Input()
    aCamera = Camera('STATIC', (12,12))
    #aCamera.block()
    aRender = Render(aCamera, DISPLAYSURF)
    #--------------------------
    unaConexion = ObtenerConexion(SoC, IP)
    if SoC == 'server':
        unMapa = Mapa('unMapa.txt')
        unMapa.enviar(unaConexion)
    else:
        unMapa = Mapa('unMapa.txt', unaConexion.recv(3660))
        
    #--------------------------
    for Char in Chars:
        toSend, Size = Char.getStringInfo()
        toSend = ':' + toSend
        unaConexion.sendall(str(Size))
        unaConexion.sendall(toSend)
    
    for Index in range(SIZE_TEAM):
        Size, data = '', ''
        while data != ':':  
            data = unaConexion.recv(1)
            Size = Size + data
        Size = Size[:-1]
        CharsEnemigos.append(creaPersonaje(unaConexion.recv(int(Size))))
    #--------------------------
    SpritesheetPisos = spritesheet("eb_piso_prueba.png")
    Piso = SpritesheetPisos.image_at((0,0,96,48),(255,255,255))
    
    while not Input.Quit:
        DISPLAYSURF.fill((0,0,0))
            
        ReadList, WriteList, xList = select.select([unaConexion],[unaConexion],[],0)
        
        if all(map(lambda x: x.Fase == FASE_A, Chars)):
            if WriteList and not MessageSent :
                for Char in Chars:
                    toSend = ''
                    toSend = toSend + Char.getTurnStringInfo() + '>'
                    Size = '<' + str(len(toSend)) + ':'
                    unaConexion.sendall(Size)
                    unaConexion.sendall(toSend)
                MessageSent = True
            if ReadList and not MessageReceived:
                for Char in CharsEnemigos:
                    data, Received = '', ''
                    while data != ':':  
                        data = unaConexion.recv(1)
                        Received = Received + data
                    Received = Received[1:].rstrip(':')
                    Size, data = 0, ''
                    while Size != int(Received):
                        data = data + unaConexion.recv(1)
                        Size += 1
                    Char.buildTurnFromString(data[:-1])
                MessageReceived = True
                        
            if all(map(lambda x: not x.Turno, Chars)) and all(map(lambda x: not x.Turno, CharsEnemigos)) and MessageReceived:
                for Char in Chars:
                    Char.cambiaFase()   
            
            if MessageSent and MessageReceived:
                for Char in Chars:
                    if Char.Turno:                        
                        Action = Char.getPlayAction()
                        if Action.Persistent:
                            ActiveActions.append(Action)
                            Char.Turno.remove(Action)
                        else:
                            Char.Play(Action)
                for Char in CharsEnemigos:
                    if Char.Turno:                        
                        Action = Char.getPlayAction()
                        if Action.Persistent:
                            ActiveActionsEnemigas.append(Action)
                            Char.Turno.remove(Action)
                        else:
                            Char.Play(Action)                        
                                    
        if all(map(lambda x: x.Fase == FASE_P, Chars)) and MessageSent and MessageReceived:            
            MessageSent = False
            MessageReceived = False
        
        
        unMapa.draw(aRender, Piso[0], Chars, CharsEnemigos)
        
        #unMapa.drawWall(aRender, "Back")
        
        Input.update()

        if CharSelected.Fase == FASE_A:
            CharSelected = Chars[(Chars.index(CharSelected)+ 1) % len(Chars)]

        if CharSelected.Fase == FASE_P:
            CharSelected.update(Input, unMapa, aCamera)
            if CharSelected.acSkill != None:
                CharSelected.acSkill.draw(aRender, 'planning')                

        for anAction in ActiveActions:
                anAction.play()
                anAction.draw(aRender)
                for Char in CharsEnemigos:
                    if Char.gotHit(anAction):
                        Char.HitPoints  -= 100
                        CharsEnemigos.remove(Char)
                if anAction.Over:
                    ActiveActions.remove(anAction)
                    
        for anAction in ActiveActionsEnemigas:
                anAction.play()
                anAction.draw(aRender)
                for Char in Chars:
                    if Char.gotHit(anAction):
                        Char.HitPoints  -= 100
                        Chars.remove(Char)
                if anAction.Over:
                    ActiveActionsEnemigas.remove(anAction)
            
        if not Chars:
            print "DEFEAT!"
            break
            
        if not CharsEnemigos:
            print "Victory!!"
            break
                    
        if CharSelected not in Chars:
            CharSelected = Chars[0]
                    
        #for char in Chars:
        #    char.draw(aRender)
            
        #for char in CharsEnemigos:
        #    char.draw(aRender)
        
        #unMapa.drawWall(aRender, "Front")
                    
        if Input.CameraOrder != None:
            aCamera.update(aCamera.xyTile |x| Input.CameraOrder)
                    
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

def roundp((x,y),n):
    return round(x,n), round(y,n)


def creaPersonaje(Info):
        Data = []
        Data = Info.split(',')
        
        if Data[0] == 'DPS':
            return DPS((int(Data[1]), int(Data[2])))
            

def ObtenerConexion(SoC, IP):
    if SoC != None:
        # Create a TCP/IP socket
        unSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        if SoC == 'server':
            server_address = ('localhost', LISTENPORT)
            unSocket.bind(server_address)
            unSocket.listen(1)
            # Wait for a connection
            connection, client_address = unSocket.accept()
            return connection

        if SoC == 'cliente':
            server_address = (IP, LISTENPORT)
            unSocket.connect(server_address)
            return unSocket


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])


