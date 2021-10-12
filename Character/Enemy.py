import pygame, random

from Props.BigHeart import BigHeart
from Props.SmallHeart import SmallHeart

class Enemy(pygame.sprite.Sprite):
    def __init__(self,nameEnemy,nFrames,width,a0,a1=0,):
        self.frameArrayMov = []
        self.imgPath='Assets/Enemy/'
        self.imgName='enemy_'
        self.image=pygame.image.load('Assets/Enemy/enemy_01.png')
        self.image.convert_alpha()
        self.moveSpeed=1
        self.attacking=False
        self.frameModulus=0
        self.currentFrame = 0   #Establece el indice del arreglo
        self.moving = True #Verifica si el enemigo esta en movimiento
        self.rect = self.image.get_rect()
        self.tempX = 0 #Pocicion futura del sprint en el eje x
        self.tempY = 0 #Pocicion futura del sprint en el eje y
        self.x = 0 #Pocicion del sprint en el eje x
        self.y = 0 #Pocicion del sprint en el eje y
        self.offset = False
        self.win = pygame.display.get_surface() #Recibira como lienzo el pygame.display.set_mode del main
        self.frameArrayMov=self.loadFrames(nFrames,nameEnemy,width,a0,a1)
        self.wallCollision = [False, False]

        self.state=True #Esta sin golpear
        self.spawned = False #Si ha sido vencido
        self.spawnedItem = 0 #Item que se genera si el enemigo es vencido
    
    def loadFrames(self,frames,name,width,a0,a1):
        array=[]
        self.image=pygame.image.load(self.imgPath + self.imgName + name  + '.png')
        for x in range(0,frames):
            numImage=width*x
            array.append(self.image.subsurface((numImage,0,a0+a1*x , self.image.get_rect().height)))
        return array
    
    def move(self, axis):
        if axis == "x":     #Cambia en el eje x
            self.x += self.moveSpeed
            self.tempX += self.moveSpeed
        # elif axis == "y":   #Cambia en el eje y
        #     self.y += self.moveSpeedY
        #     self.tempY = self.y      
    
    def setOffset(self, x, y, state): #Define un offset entre las variables temp y las pociciones
        toggle = state
        if self.offset == False and toggle:
            self.offset = True
            self.tempX = self.x
            self.tempY = self.y
            self.x += x
            self.y += y
        if toggle == False:
            self.x = self.tempX
            self.y = self.tempY
            self.offset = False

    def setDirection(self):
        if self.moveSpeed < 0:
            
            self.setOffset(-50, 0, False)
            # self.attackBox.setPos(self.x + 100, self.y + 12)
            # self.passiveBox.setPos(self.x + self.hitBoxOffsetX[0], self.y + self.hitBoxOffsetY[0])
        else:
           
            self.setOffset(0, 0, True) #Genera ofset entre las variables temp y de pocicion
            # self.attackBox.setPos(self.x, self.y + 12)
            # self.passiveBox.setPos(self.x + self.hitBoxOffsetX[1], self.y + self.hitBoxOffsetY[1])
            self.image = pygame.transform.flip(self.image, True, False) #Carga la imagen de manera simetrica en el eje x

    def setMove(self, state): #Establece si belmont se mueve o no
        self.moving = state
    
    def setPos(self, x, y): #Establece la pocicion del sprint
        self.x = x
        self.y = y
        self.tempX = x
        self.tempY = y
    
    def checkWall(self):

        if self.x <= -40 :
            self.wallCollision[0] = True
        else:
            self.wallCollision[0] = False


        if self.y > 244 and self.y <= 340:

            if self.x <= 36 :
                self.wallCollision[0] = True
            else:
                self.wallCollision[0] = False

        if self.x >= 514 :
            self.wallCollision[1] = True
        else:
            self.wallCollision[1] = False

        if self.wallCollision[0]:

            self.moveSpeed=-self.moveSpeed

        if self.wallCollision[1]:
        
            self.moveSpeed=-self.moveSpeed

    def setSpeed(self, amount, axis): #Establece la velocidad de movimiento
        if axis == "x":         #Verifica en que eje se modifica la velocidad
            self.moveSpeed = amount  #Establece la velocidad de movimiento en el eje x
        elif axis == "y":
            self.moveSpeedY = amount #Establece la velocidad de movimiento en el eje y

    def getPos(self): #Te da la pocicion del enemigo
        array = [self.x, self.y]
        return array

    def getRect(self): #Te da el ancho y el largo del enemigo
        array = [self.rect.width, self.rect.height]
        return array

    def getSpawnedItem(self):  #Retorna el item dado al vencer al enemigo
        return self.spawnedItem     #al ser golpeado retorna esto

    def getState(self):  #Te da el estado del enemigo
        return self.state

    def setActive(self, state):
        self.state = state

        if self.state == False and self.spawned == False:
            self.spawnItem()
            self.spawned = True

    def spawnItem(self):        #genera el corazon , con asignacion random
        rnd = random.randint(0,3)

        if rnd == 0:
            self.spawnedItem = BigHeart(self.x, self.y)

        if rnd > 0:
            self.spawnedItem = SmallHeart(self.x, self.y)


    def playAnim(self, anim):
        if anim == "idle":
            self.image = self.frameArrayMov[0]
           

        if anim == "walk":
            mod = self.frameModulus%10
            if mod==0:
                self.currentFrame += 1
            if(self.currentFrame>len(self.frameArrayMov)-1):
                self.currentFrame=0

            self.frameModulus += 1
            self.image = self.frameArrayMov[self.currentFrame]

        

        

        self.setDirection()
        self.checkWall()


    def update(self):
        if self.state: #Sin golpear

            self.tempY = self.y
            if self.moving:
                self.move("x")
                
                if self.attacking == False:
                    self.playAnim("walk")
                # if self.attacking:
                #      self.playAnim("attack")
            else:
                if self.attacking == False:
                    self.playAnim("idle")

                # if self.attacking:
                #     self.playAnim("attack")


            # if self.getNumberOfCollisions() == 0:
            #     self.setFloor(340)

            
            self.win.blit(self.image, (self.x, self.y)) #Actualiza el sprint de acuerdo las condiciones
            # self.collisionArray = []
            # self.updateCollision()
            # self.attackBox.update()
            # self.passiveBox.update()
            
            #self.attackBox.getHit(self.x, self.y, self.rect.width, self.rect.height)
        elif self.spawned:  #golpeado y genera item
            self.spawnedItem.update()  #Genera item  actualiza