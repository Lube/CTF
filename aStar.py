import sets

Libre = '#'
Ocupado = '0'
def distancia(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1]) #Valor absoluto.

def vecinos(Mapa, (a,b)):
    vecinos = []
    if a+1 < len(Mapa) and Mapa[a+1][b] == Libre:
        vecinos.append((a+1,b))
    if a-1 > 0 and Mapa[a-1][b] == Libre:
        vecinos.append((a-1,b))
    if b+1 < len(Mapa[0]) and Mapa[a][b+1] == Libre:
        vecinos.append((a,b+1))
    if b-1 > 0 and Mapa[a][b-1] == Libre:
        vecinos.append((a,b-1))
    
    return vecinos
        
class Nodo:
    def __init__(self, pos, Fin, padre=None):
        self.pos = pos
        self.padre = padre
        self.h = distancia(self.pos, Fin)
 
        if self.padre == None:
            self.g = 0
        else:
            self.g = self.padre.g + 1
        self.f = self.g + self.h

def aStar (Mapa, Inicio, Fin):
    openSet = set()
    closedSet = set()
    
    openSet.add(Nodo(Inicio, Fin))
    
    while len(openSet) > 0:
        Inicio = min(openSet, key=lambda inst:inst.h)
        if Inicio.pos == Fin:
            return True
        openSet.remove(Inicio)
        closedSet.add(Inicio)
        for tile in vecinos(Mapa, Inicio.pos): 
            if tile not in getTiles(closedSet):
                aNodo= Nodo(tile, Fin)
                if tile not in getTiles(openSet):
                    openSet.add(aNodo)
                aNodo.padre = Inicio
    return False

def getTiles(set):
    l = []
    for x in set:
        l.append(x.pos)
    return l




