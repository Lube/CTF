import random, sys, pygame

LINE = 0
SQR = 1

class skillshot():
    efRate = 0
    disRate = 0
    pattern = []
    avPatterns = []
    pos = (0,0)
    mouse = input.mouse()
    facing = input.mouseDirection()

    def __init__(self, efRate,disRate, pos):
        self.efRate = efRate
        self.disRate = disRate
        self.pos = pos

    def update(self, pattern):
        prev = (0,0)
        if pattern == LINE:
            for i in range(self.disRate):
                prev= tuple(map(sum, zip(prev, self.facing)))
                self.pattern.append(prev)
        if pattern == SQR:
            prev = self.mouse
            if input.Rotate():
                self.rotate()
            for i in range(self.disRate/2):
                prev = tuple(map(sum, zip(prev, self.facing)))
                self.pattern.append(prev)
            for double in self.pattern:
                if self.facing in (RIGHT, LEFT):
                    self.pattern.append(x,y+1)
                if self.facing in (UP, DOWN):
                    self.pattern.append(x+1,y)

    def rotate(self):
        if self.facing == RIGHT:
            self.facing = DOWN
        if self.facing == DOWN:
            self.facing = LEFT
        if self.facing == LEFT:
            self.facing = UP
        if self.facing == UP:
            self.facing = RIGHT



