import pygame

from Collision.Attack import AttackBox
from Collision.Passive import PassiveBox

class Belmont(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.attacking = False #Verifica si esta atacando
        self.crouchFrame = pygame.image.load('Assets/Belmont/Belmont_Crouch.png') #Carga el frame de belmont agachado
        self.crouching = False #Define si belmont esta agachado
        self.currentFrame = 0 #Especifica el current fram
        self.fallSpeed = 3  #Define la Velocidad de caida
        self.frameArrayWalk = [] #Array de Belmont Caminando
        self.frameArrayAttack = [] #Array de Belmont atacando
        self.frameModulus = 0 #Modulo del movimiento de Belmont
        self.gravity = 1 #Define la gravedad del juego
        self.jumping = False #Define si belmotn esta saltando
        self.jumpAndMove = False #Define si belmont esta atacando y saltando a la vez
        self.jumpForce = -12 #Define la fuerza del salto
        self.jumpPush = -12 #Define la fuerza de caida
        self.jumpFrame = pygame.image.load('Assets/Belmont/Belmont_Jump.png') #Carga el frame de belmont saltando
        self.heartCount = 0 #Contador de corazones
        self.imageDir = True #Define la direccion de movimiento del frame
        self.imgPath = 'Assets/Belmont/' #Direccion de los frames de belmont
        self.imgName = 'Belmont_' #El nombre del frame de Belmont
        self.image = pygame.image.load('Assets/Belmont/Belmont_Walk_01.png') #Carga el frame actual de belmont
        self.image.convert_alpha() 
        self.keyDown = [False, False] #Define si se esta presionando una tecla izquierda o derecha
        self.moving = False #Define si se esta moviendo Belmont
        self.moveDir = True  #Define si belmont esta en movimiento en el eje x
        self.moveSpeed = 1 #Velocidad de movimiento de Belmont
        self.moveSpeedY = 0 #Velocidad de movimiento en el eje Y
        self.offset = False #Offset entre las variabls temp y las pociciones actuales
        self.rect = self.image.get_rect()    #area de la imagen belmon_Walk_01
        self.tempX = 0  #Variable temp en eje x
        self.tempY = 0 #Variale temp en eje y
        self.x = 0 #Pocicion actual en el eje x
        self.y = 0 #Pocicion actual en el eje y
        self.win = pygame.display.get_surface() #Define la superficio en la que se trabajara

        self.floor = self.y  #Define la pocicion del piso

        self.collisionArray = []  #Los objetos de colicion
        self.wallCollision = [False, False] #Si esta en los limites del movimiento permitido

        self.frameArrayWalk = self.loadFrames(3, 'Walk_0') #Carga los arrays de Belmont caminando
        self.frameArrayAttack = self.loadFrames(3, 'Attack_0') #Carga los array de Belmont atacando
        self.frameArrayAttackCrouch = self.loadFrames(3, 'AttackCrouch_0') #Carga los array de Belmont atando agachado

        self.hitBoxX = 40 #Define los rangoz en X para la colicion
        self.hitBoxY = 59 #Define los rangos en Y para la colicion
        #valores para calibrar
        self.hitBoxOffsetX = [28, 88] #Define los offsets en caso no se mueva o se mueva
        self.hitBoxOffsetY = [1, 1] #Define los offsets en caso se mueva o no se mueva

        self.attackBox = AttackBox(self.x + 100, self.y + 11, 60, 27) #Define el rango del ataque
        #posicion y tamaño en PassiveBox
        self.passiveBox = PassiveBox(self.x + self.hitBoxOffsetX[0], self.y + self.hitBoxOffsetY[0], self.hitBoxX, self.hitBoxY) #Define el rango que ocupa belmont

    def loadFrames(self, frames, name):
        array = []
        for x in range(0, frames):
            numImage = x + 1
            array.append(pygame.image.load(self.imgPath + self.imgName + name + str(numImage) + '.png'))
        return array

    def move(self, axis):
        if axis == "x":
            self.x += self.moveSpeed
            self.tempX += self.moveSpeed
        elif axis == "y":
            self.y += self.moveSpeedY
            self.tempY = self.y

    def getHeartCount(self):
        return self.heartCount

    def addHeartToCount(self, n):
        self.heartCount += n

    def addCollision(self, obj):
        self.collisionArray.append(obj)

    def getNumberOfCollisions(self):
        return len(self.collisionArray)

    def initAttack(self):
        if self.attacking == False:
            self.setMove(False)
            self.attacking = True
            self.currentFrame = 0

    def initCrouch(self):
        if self.crouching == False:
            self.crouching = True

    def initJump(self):
        if self.jumping == False:
            if self.y == self.floor:
                self.jumping = True

            if self.moving:
                self.jumpAndMove = True

    def getJumpState(self):
        return self.jumping

    def getAttackState(self):
        return self.attacking

    def getKeyState(self, key):
        if key == "left":
            return self.keyDown[0]
        elif key == "right":
            return self.keyDown[1]

    def getPos(self):
        array = [self.x, self.y]
        return array

    def getRect(self):
        array = [self.rect.width, self.rect.height]
        return array

    def checkJump(self):
        if self.jumping:
            self.setSpeed(self.jumpForce, "y")
            self.move("y")
            self.jumpForce += self.gravity

            if self.jumpAndMove:
                self.setMove(True)

        if self.y > self.floor:

            if self.jumpAndMove:
                if self.keyDown[0] == False and self.keyDown[1] == False:
                    self.setMove(False)
                self.jumpAndMove = False

            if self.keyDown[0] and self.attacking == False:
                self.setMove(True)
                self.setSpeed(-2, "x")

            if self.keyDown[1] and self.attacking == False:
                self.setMove(True)
                self.setSpeed(2, "x")

            if self.keyDown[0] == False and self.keyDown[1] == False:
                self.setMove(False)

            if self.attacking:
                self.setMove(False)

            self.y = self.floor
            self.jumping = False
            self.jumpForce = self.jumpPush

        if self.jumpForce <= 0 and self.attacking == False:
            if self.jumping:
                self.playAnim("jump")
        elif self.y < self.floor and self.attacking == False:
            self.playAnim("idle")

    def checkWall(self):
        if self.x <= -88 and self.imageDir == False:
            self.wallCollision[0] = True
        elif self.x <= -40 and self.imageDir:
            self.wallCollision[0] = True
        else:
            self.wallCollision[0] = False


        if self.y > 244 and self.y <= 340:
            if self.x <= -22 and self.imageDir == False:
                self.wallCollision[0] = True
            elif self.x <= 36 and self.imageDir:
                self.wallCollision[0] = True
            else:
                self.wallCollision[0] = False

        if self.x >= 514 and self.imageDir:
            self.wallCollision[1] = True
        elif self.x >= 514 and self.imageDir == False:
            self.wallCollision[1] = True
        else:
            self.wallCollision[1] = False

        if self.wallCollision[0]:
            if self.imageDir == False:
                self.x = -87
                self.tempX = self.x
                if self.y > 244 and self.y <= 340:
                    self.x = -21
                    self.tempX = self.x
            elif self.imageDir:
                self.x = -28
                self.tempX = self.x
                if self.y > 244 and self.y <= 340:
                    self.x = 37
                    self.tempX = self.x

        if self.wallCollision[1]:
            if self.imageDir == False:
                self.x = 460
                self.tempX = 460
            elif self.imageDir:
                self.x = 513
                self.tempX = 513

    def fall(self):
        if self.y < self.floor:
            self.setSpeed(self.fallSpeed, "y")
            self.move("y")
            self.fallSpeed += self.gravity
        else:
            self.fallSpeed = 3

    def setKeyDown(self, key, state):
        if key == "left":
            self.keyDown[0] = state
        elif key == "right":
            self.keyDown[1] = state


    def setMove(self, state):
        self.moving = state

    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.tempX = x
        self.tempY = y

    def setFloor(self, floor):
        self.floor = floor

    def setSpeed(self, amount, axis):
        if axis == "x":
            self.moveSpeed = amount
        elif axis == "y":
            self.moveSpeedY = amount

    def getSpeed(self, axis):
        if axis == "x":
            return self.moveSpeed
        elif axis == "y":
            return self.moveSpeedY

    def setOffset(self, x, y, state):
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
        if self.moveSpeed > 0:
            self.imageDir = True
            self.setOffset(0, 0, False)
            self.attackBox.setPos(self.x + 100, self.y + 12)
            self.passiveBox.setPos(self.x + self.hitBoxOffsetX[0], self.y + self.hitBoxOffsetY[0])
        else:
            self.imageDir = False

        if self.imageDir == False:
            self.setOffset(-50, 0, True)
            self.attackBox.setPos(self.x, self.y + 12)
            self.passiveBox.setPos(self.x + self.hitBoxOffsetX[1], self.y + self.hitBoxOffsetY[1])
            self.image = pygame.transform.flip(self.image, True, False)

    def stopCrouch(self):
        if self.crouching:
            self.crouching = False

    def playAnim(self, anim):
        if anim == "idle":
            self.image = self.frameArrayWalk[0]
            self.currentFrame = 0

        if anim == "walk":
            mod = self.frameModulus%5

            if mod == 0:
                self.currentFrame += 1

            if (self.currentFrame > 2):
                self.currentFrame = 1

            self.frameModulus += 1
            self.image = self.frameArrayWalk[self.currentFrame]

        if anim == "jump":
            self.image = self.jumpFrame

        if anim == "crouch":
            if self.currentFrame == 0:
                self.image = self.crouchFrame

        if anim == "attack":
            mod = self.frameModulus%5

            if mod == 0:
                self.currentFrame += 1

            if self.currentFrame > 1:
                self.attackBox.toggleActive(True)

            if self.currentFrame > 2:
                self.currentFrame = 2

                if self.keyDown[0]:
                    self.setMove(True)
                    self.setSpeed(-2, "x")

                elif self.keyDown[1]:
                    self.setMove(True)
                    self.setSpeed(2, "x")

                self.attacking = False
                self.attackBox.toggleActive(False)

            self.frameModulus += 1

            self.image = self.frameArrayAttack[self.currentFrame]

        if anim == "attackCrouch":
            mod = self.frameModulus%5

            if mod == 0:
                self.currentFrame += 1

            if self.currentFrame > 1:
                self.attackBox.toggleActive(True)

            if self.currentFrame > 2:
                self.currentFrame = 2

                if self.keyDown[0]:
                    self.setMove(True)
                    self.setSpeed(-2, "x")

                elif self.keyDown[1]:
                    self.setMove(True)
                    self.setSpeed(2, "x")

                self.attacking = False
                self.attackBox.toggleActive(False)

            self.frameModulus += 1

            self.image = self.frameArrayAttackCrouch[self.currentFrame]


        self.setDirection()
        self.checkWall()

    def updateCollision(self):
        if self.imageDir:
            if self.crouching:
                self.attackBox.setPos(self.x + 100, self.y + 27)
                self.passiveBox.changeSize(self.hitBoxX, self.hitBoxY - 20)
                self.hitBoxOffsetY[0] = 21
            else:
                self.attackBox.setPos(self.x + 100, self.y + 12)
                self.passiveBox.changeSize(self.hitBoxX, self.hitBoxY)
                self.hitBoxOffsetY[0] = 1

            self.passiveBox.setPos(self.x + self.hitBoxOffsetX[0], self.y + self.hitBoxOffsetY[0])

        if self.imageDir == False:
            if self.crouching:
                self.attackBox.setPos(self.x, self.y + 12)
                self.passiveBox.changeSize(self.hitBoxX, self.hitBoxY - 20)
                self.hitBoxOffsetY[1] = 21
            else:
                self.attackBox.setPos(self.x, self.y + 27)
                self.passiveBox.changeSize(self.hitBoxX, self.hitBoxY)
                self.hitBoxOffsetY[1] = 1

            self.passiveBox.setPos(self.x + self.hitBoxOffsetX[1], self.y + self.hitBoxOffsetY[1])

    def update(self):
        self.tempY = self.y
        if self.moving:
            self.move("x")
            if self.keyDown[0] or self.keyDown[1]:
                if self.attacking == False:
                    self.playAnim("walk")
            if self.jumping and self.attacking:
                self.playAnim("attack")
        else:
            if self.jumping == False and self.attacking == False:
                self.playAnim("idle")

            if self.attacking and self.crouching == False:
                self.playAnim("attack")

            if self.crouching and self.attacking:
                self.playAnim("attackCrouch")
            elif self.crouching and self.attacking == False:
                self.playAnim("crouch")

        if self.jumping == False:
            self.fall()

        if self.getNumberOfCollisions() == 0:
            self.setFloor(340)

        self.checkJump()
        self.win.blit(self.image, (self.x, self.y))
        self.collisionArray = []
        self.updateCollision()
        self.attackBox.update()
        self.passiveBox.update()
        #self.attackBox.getHit(self.x, self.y, self.rect.width, self.rect.height)
