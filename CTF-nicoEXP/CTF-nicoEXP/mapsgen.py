import random, pygame, sys

STONE_M = 0
STONE_COR = 1
STONE_MU = 2
STONE_OFF = 3
BORD_TRI = 100
BORD_DOB = 60
BORD_SIM = 30
BORD_NO = 0
ALLFORMS = [STONE_M, STONE_COR, STONE_MU, STONE_M, STONE_COR, STONE_MU, STONE_M, STONE_COR, STONE_MU, STONE_M, STONE_COR, STONE_MU, STONE_OFF]



class oMap():
    size = (60, 60)
    mapList = []
    Map = ''
    def __init__(self, size = (60,60)):
        """junta las 4 partes del mapa, las convierte en string y guarda en
        unmapa.txt """
        self.size = size
        top = []
        bot = []
        #Divide el mapa en 4 partes y genera cada parte
        topLeft = partsFactory.getPart(self)
        topRight = partsFactory.getPart(self)
        botLeft = partsFactory.getPart(self)
        botRight = partsFactory.getPart(self)
        #separa el mapa en top y bot
        for column in range(len(topLeft)):
            top.append(topLeft[column]+topRight[column])
        for column in range(len(botLeft)):
            bot.append(botLeft[column]+botRight[column])
        self.mapList = top+bot
        #le pone bordes horizontales
        self.borders()
        #y verticales
        #lo transforma en string
        for column in self.mapList:
            for tile in column:
                self.Map+= tile
            self.Map+='\n'
        #lo guarda en el archivo.
        readableMap = open('unmapa.txt', 'a')
        readableMap.write(self.Map)
        readableMap.close()

    def borders(self):
        """pone  bordes al mapa"""
        firstMap = []
        finalMap = []
        for column in self.mapList:
            startBorder = random.randint(1,100)
            endBorder = random.randint(1,100)
            if startBorder <= BORD_SIM and startBorder > BORD_NO:
                column[0]= '0'
            if startBorder <= BORD_DOB and startBorder > BORD_SIM:
                column[0:2] = ['0', '0']
            if startBorder <= BORD_TRI and startBorder > BORD_DOB:
                column[0:3] = ['0','0','0']
            if endBorder <= BORD_SIM and endBorder > BORD_NO:
                column[-1]= '0'
            if endBorder <= BORD_DOB and endBorder > BORD_SIM:
                column[-2:] = ['0','0']
            if endBorder <= BORD_TRI and endBorder > BORD_DOB:
                column[-3:] = ['0','0','0']
            firstMap.append(column)
        inverted = map(list, zip(*firstMap))
        for column in inverted:
            startBorder = random.randint(1,100)
            endBorder = random.randint(1,100)
            if startBorder <= BORD_SIM and startBorder > BORD_NO:
                column[0]= '0'
            if startBorder <= BORD_DOB and startBorder > BORD_SIM:
                column[0:2] = ['0', '0']
            if startBorder <= BORD_TRI and startBorder > BORD_DOB:
                column[0:3] = ['0','0','0']
            if endBorder <= BORD_SIM and endBorder > BORD_NO:
                column[-1]= '0'
            if endBorder <= BORD_DOB and endBorder > BORD_SIM:
                column[-2:] = ['0','0']
            if endBorder <= BORD_TRI and endBorder > BORD_DOB:
                column[-3:] = ['0','0','0']
            finalMap.append(column)
        self.mapList = finalMap

class factory(object):

    def getPart(self, Map):
        """random pattern factory"""
        partHeight = Map.size[1]/2
        partWidth = Map.size[0]/2
        part = [['#' for x in range(partWidth)]for y in range(partWidth)]

        #elige el pattern
        part_pattern = random.choice(ALLFORMS)

        #lo aplica y devuelve
        if part_pattern == STONE_M:
            mapped = stoneMid((int(partWidth/2), int(partHeight/2)),random.randint(partHeight/7.5,partHeight/3),random.randint(partWidth/7.5,partWidth/3))#IKR modificala si podes :C
            mapped.draw(part)
        if part_pattern == STONE_COR:
            avCorners = ['TL', 'TR', 'BL', 'BR']
            corner = random.choice(avCorners)
            if corner == 'TL' or corner == 'TR':
                top = random.randint(1, int(partHeight/3))
            else:
                top = random.randint(int(partHeight/2), partHeight-int(partHeight/3))

            if corner == 'TL' or corner == 'BL':
                left = random.randint(1,int(partWidth/3))
            else:
                left = random.randint(int(partWidth/2), partWidth-int(partWidth/3))
            mapped = stoneCor((left,top),random.randint(int(partHeight/7.5),int(partHeight/3)), random.randint(int(partWidth/7.5),int(partWidth/3)))
            mapped.draw(part)
        if part_pattern == STONE_MU:
            nStones= random.randint(2,4)
            for stone in range(nStones):
                mapped = stoneMu(int(partHeight/nStones),int(partWidth/nStones),(random.randint(1, partHeight-(int(partHeight/nStones)+1)), random.randint(1, partHeight-int(partHeight/nStones+1)))) #esta linea es cancer, lo s?, si se te ocurre como alindarla hacelo xD
                mapped.draw(part)
        if part_pattern == STONE_OFF:
            return part
        return part





class stone():
    width = 0
    height = 0
    center = (0,0)
    def __init__(self, width, height, center):
        self.width = width
        self.height = height
        self.center = center

    def draw(self, part):
        """crea las 'piedras'"""
        #hace una X de (X-rockwidth/2:X+rockwidth/2) y lo mismo con Y
        X, Y = self.center
        for i in range(int(Y-self.height/2), int(Y+self.height/2)):
            part[i][Y] = '0'
        for j in range(int(X-self.width/2), int(X+self.width/2)):
            part[X][j] = '0'
        #chequea los tiles que rodean al nuestro y genera una chance de que ahi haya roca
        for column in range(Y-self.height, Y+self.height):
            for tile in range(X-self.width, X+self.width):
                if column > 28:
                    column = column-(column-28)
                if tile > 28:
                    tile = tile-(tile-28)
                if part[column][tile] == '#':
                    rockChances = 0
                    if part[column-1][tile] == '0':
                        if rockChances == 0:
                            rockChances += 40
                        else:
                            rockChances += rockChances/1.5
                    if part[column+1][tile] == '0':
                        if rockChances == 0:
                            rockChances += 40
                        else:
                            rockChances += rockChances/1.5
                    if part[column][tile-1] == '0':
                        if rockChances == 0:
                            rockChances += 40
                        else:
                            rockChances += rockChances/1.5
                    if part[column][tile+1] == '0':
                        if rockChances == 0:
                            rockChances += 40
                        else:
                            rockChances += rockChances/1.5
                    nextTile = random.randint(0,100)
                    #genera la roca
                    if nextTile < rockChances:
                        part[column][tile] = '0'
                    else:
                        part[column][tile] = '#'
        return part

class stoneMid(stone):
    def __init__(self, center, height,width):
        """si la pattern es 'STONE_M' elige la altura y el ancho de la piedra y la crea"""
        self.height = height
        self.width = width
        self.center = center

class stoneCor(stone):
    def __init__(self, center, height, width):
        """si la pattern es 'STONE_COR' elige en que esquina hacer la piedra
        y el tamanio y la crea."""
        self.height = height
        self.width = width
        self.center = center

class stoneMu(stone):
    def __init__(self, height, width, center):
        """si el patern es 'STONE_MU' elije el numero de piedras y el tama?o que tiene y las crea"""
        self.height = height
        self.width = width
        self.center = center

partsFactory = factory()





