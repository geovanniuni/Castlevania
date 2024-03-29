import pygame

class  AttackBox (pygame.sprite.Sprite):

    def __init__(self, x, y, sizeX, sizeY):
        self.x = x
        self.y = y
        self.sX = sizeX
        self.sY = sizeY
        self.color = pygame.Color(255,0,0)
        self.win = pygame.display.get_surface()
        self.state = False
        self.surface = pygame.Surface((self.sX, self.sY))
        self.surface.fill(self.color)
        
    def getHit(self, tx, ty, sX, sY, obj):
        right = self.x + self.sX
        bottom = self.y + self.sY
        
        tRight = tx + sX
        tBottom = ty + sY
        
        if self.x <= tRight and right >= tx and self.y <= tBottom and bottom >= ty:
            if self.state:
                obj.setActive(False)

            
    def setPos(self, x, y):
        self.x = x
        self.y = y
        
    def toggleActive(self, state):
        self.state = state
            
    def update(self):
        pass