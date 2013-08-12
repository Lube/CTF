import pygame, random, sys, time, eb_char
from pygame.locals import *
from eb_lectormapa import *

dClavesMapa= {1:BLACK, 0:WHITE}

#           R,    G,    B
BLACK =     (0  , 0  ,  0  )
WHITE =     (255, 255,  255)
GREEN =     (0  , 160,  50 )
RED   =     (160, 25 ,  25 )

def main():
    global DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((1024, 720))
    pygame.display.set_caption('eb_int')
    #-----------------#
    background = pygame.image.load("Dibujo.bmp")#
    background.set_colorkey(WHITE)
    backgroundRect = background.get_rect()
    unMapa = Mapa('unMapa.txt')
    inp = inputBoard()
    disp = displayBoard()
    but = buttons()
    minimapa = MiniMap(unMapa)
    #-----------------#
    while True:
        DISPLAYSURF.fill((0,125,0))#green
        inp.update()
        if not inp.isActive:
            if inp.Mensaje == '/clear':
                disp.clear()            
            disp.abajo = ''
            disp.update(inp.Mensaje)
            inp.Mensaje = ''
        else:
            disp.abajo = inp.Mensaje
        but.update()
        DISPLAYSURF.blit(background, backgroundRect)
        DISPLAYSURF.blit(minimapa.draw(), (895,593))
        if inp.isActive:
            DISPLAYSURF.blit(disp.draw(0,0), (5,550))
        else:
            if inp.countDown > 0:
                inp.countDown -= 1
                DISPLAYSURF.blit(disp.draw(0,0), (5,550))
                
        pygame.display.update()
        FPSCLOCK.tick(30)

class MiniMap(object):
    def __init__(self, Mapa, Chars =[] ):
        self.Surface = MiniMap.GenerarSurface(Mapa)
        if Chars:
            self.updateChars(Chars)

    def updateChars(self, Chars):
        paSurface = pygame.PixelArray(self.Surface)
        for Char in Chars:
            paSurface[Char.Posicion[0]][Char.Posicion[1]] = RED

    def draw(self):
        return self.Surface



    @classmethod
    def GenerarSurface(self, Mapa):
        aSurface = pygame.Surface((Mapa.fil*2, Mapa.col*2))
        paSurface = pygame.PixelArray(aSurface)

        for Fila in range(Mapa.fil * 2):
            for Col in range(Mapa.col * 2):
                paSurface[Fila][Col] = dClavesMapa[Mapa.mapa[Fila//2][Col//2]]
        return aSurface



class inputBoard():
    Mensaje = ""

    def __init__(self):
        self.isActive = False
        self.countDown = 0

    def update(self):
        if not self.isActive:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_RETURN:
                        self.isActive = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ',
                                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K','L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                                         '!', '?', '0', '1','2','3', '4', '5', '6', '7', '8','9','-','.', ',', ';', ':', '_', "'", '"', '#', '*', '/','+', '=', '@', '(', ')', '$','?', '?', '&', '%']:
                        self.Mensaje = self.Mensaje + str(event.unicode)
                    if event.key == K_RETURN:
                        self.isActive = False
                        self.countDown = 50
                    if event.key == K_BACKSPACE:
                        self.Mensaje = self.Mensaje[:-1]
                        

        


class displayBoard():

    text = []
    Surface = None
    abajo = ''
    def __init__(self):
        self.Surface = pygame.Surface((333,164))
        self.Surface.set_alpha(100)
        self.font = pygame.font.Font(None, 12)

    def update(self, line):
        if line != '':
            if len(self.text) > 7:
                self.text = self.text[1:]
            self.text.append(line)

    def clear(self):
        self.text = []

    def draw(self, x, y):
        self.Surface.fill((0, 0, 0))
        self.Surface.set_alpha(150)

        for i, Line in enumerate(self.text):
            text = self.font.render(Line, 3, (255, 255, 255))
            text.set_alpha(150)
            textPos = text.get_rect()
            self.Surface.blit(text, (x,y+i*15))

        if self.abajo:
            text = self.font.render(self.abajo, 3, (255, 255, 255))
            text.set_alpha(150)
            textPos = text.get_rect()
            self.Surface.blit(text, (0,152))


        return self.Surface

class party():
    pass

class buttons():
    def __init__(self):
        self.actual = False
        self.disp =  pygame.Surface((1024,720))
        self.boardSize = (0,0)
        self.stButtons = {0:(875,599), 1:(875, 620), 2:(875,643)}
        self.disp.set_colorkey(WHITE)
        self.disp.fill(WHITE)
    def update(self):
        #----------
        w, h = self.boardSize
        if  not self.actual:
            w,h = None, None
        else:
            for i in range(551):
                w = i
                h = 129
                board = pygame.Rect((i if i <=342 else 342, 587),(w,h))
                board.fill(GREEN)
                self.disp.blit(board, board.topleft)
        #----------
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bt in stButtons:
                    pos = pygame.mouse.get_pos()
                    x,y = stButtons[bt]
                    if pos[0] - x <= 9 and pos[1] - y <= 9:
                        if not self.actual:
                            self.actual = True
                        else:
                            self.actual = False
        #---DRAW---
        self.render()
        
    def render(self):
        for i in self.stButtons:
            pygame.draw.circle(DISPLAYSURF, RED, self.stButtons[i], 9, 5)
        DISPLAYSURF.blit(self.disp, (0,0))




if __name__ == '__main__':
    main()
