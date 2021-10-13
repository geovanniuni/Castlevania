import pygame, sys
from pygame.locals import *

from Character.Belmont import Belmont
from Props.Candle import Candle
from Collision.Platform import PlatformBox
from Stage.Stage import Stage
from UI.UI import UI_Image
from UI.UI import UI_Text

class GameState():
    def __init__(self, level, player,squelet ,bird ,fpsLimit,candleGroup_1,platformGroup_1,candleGroup_2,platformGroup_2,  UI_Top, UI_HeartCount, UI_Time,runTime ,UI_Score, UI_TextGroup, score):
        self.level = level
        self.player = player
        self.squelet= squelet
        self.bird = bird
        self.fpsLimit = fpsLimit
        self.candleGroup_1= candleGroup_1
        self.platformGroup_1 = platformGroup_1
        self.candleGroup_2 = candleGroup_2
        self.platformGroup_2 = platformGroup_2
        self.UI_Top = UI_Top
        self.UI_HeartCount = UI_HeartCount
        self.UI_Time = UI_Time
        self.runTime = runTime
        self.UI_Score = UI_Score
        self.UI_TextGroup = UI_TextGroup
        self.score=score




    def main_game(self, candleGroup , platformGroup):
        self.candleGroup = candleGroup
        self.platformGroup = platformGroup

        #1 for
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RIGHT:
                    self.player.setKeyDown("right", True)
                    if self.player.getJumpState() == False and self.player.getAttackState() == False:
                        self.player.setMove(True)
                        self.player.setSpeed(2, "x")
                elif event.key == K_LEFT:
                    self.player.setKeyDown("left", True)
                    if self.player.getJumpState() == False and self.player.getAttackState() == False:
                        self.player.setMove(True)
                        self.player.setSpeed(-2, "x")
                if event.key == K_z:
                    self.player.initAttack()
                if event.key == K_DOWN:
                    self.player.initCrouch()
                if event.key == K_SPACE:
                    self.player.initJump()

            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.player.setKeyDown("right", False)
                    if self.player.getKeyState("left") == False:
                        self.player.setMove(False)

                elif event.key == K_LEFT:
                    self.player.setKeyDown("left", False)
                    if self.player.getKeyState("right") == False:
                        self.player.setMove(False)

                if event.key == K_DOWN:
                    self.player.stopCrouch()

        self.fpsLimit.tick(30)

        self.player.update()
        self.squelet.update()
        self.bird.update()

        #2 for

        


      
        for x in self.candleGroup:
            pos = x.getPos()   #Array de las posisiones de candle
            rect = x.getRect()  #Array de las longitudes de rect a las imagnes

            #x como objecto
            #le enviamos la posicion de los candelabros, medidas del recuadro y el candelabro(ultimo?)

            self.player.attackBox.getHit(pos[0], pos[1], rect[0], rect[1], x)
            #update de candelabros -->animacion
            x.update()

            #NO SE COMPILA ESTO AL COMIENZO
            if x.getState() == False:  #si es golpeado el candelabro
                item = x.getSpawnedItem()    # se genera un item --retorna un 0?
                iPos = item.getPos()         #Posicion e rect del item
                iRect = item.getRect()

                self.player.passiveBox.getHit(iPos[0], iPos[1], iRect[0], iRect[1], item)

                if item.getState() == False and item.getPickedUpState() == False:
                    item.pickUp()
                    self.player.addHeartToCount(item.getHeartValue())

                for y in self.platformGroup:
                    jPos = y.getPos()
                    jRect = y.getRect()
                    if iPos[0] > jPos[0] and iPos[0] < (jPos[0] + jRect[0]):
                        item.setFloor(jPos[1] + jRect[1] - iRect[1])
        #3 for
        for x in self.platformGroup:
            #obtenemos informacion de los box
            #en belmont invoca al metodo passive box ->obtener los valores de posicion nada mas [x,y]
            pos = self.player.passiveBox.getPos()

            #Analiza si golpeo  a las plataformas---suelo?---> brinda y
            bottom = x.getHit(pos[0], pos[1], 40, 59)
            x.update()

            #Si golpea algo , es true y entra al if
            if x.getCollision():
                pPos = self.player.getPos() #[x,y]
                if pPos[1] <= bottom:
                    self.player.setFloor(bottom)  #define el suelo con el valor de bottom
                    self.player.addCollision(x)   #

        self.UI_Top.update()

        pos_enemy=self.squelet.getPos()
        rect_enemy=self.squelet.getRect()
        self.player.attackBox.getHit(pos_enemy[0], pos_enemy[1], rect_enemy[0], rect_enemy[1], self.squelet)

        if self.squelet.getState() == False:  #si es golpeado el candelabro
                item = self.squelet.getSpawnedItem()    # se genera un item --retorna un 0?
                iPos = item.getPos()         #Posicion e rect del item
                iRect = item.getRect()

                self.player.passiveBox.getHit(iPos[0], iPos[1], iRect[0], iRect[1], item)

                if item.getState() == False and item.getPickedUpState() == False:
                    item.pickUp()
                    self.player.addHeartToCount(item.getHeartValue())

                for y in self.platformGroup:
                    jPos = y.getPos()
                    jRect = y.getRect()
                    if iPos[0] > jPos[0] and iPos[0] < (jPos[0] + jRect[0]):
                        item.setFloor(jPos[1] + jRect[1] - iRect[1])




        pos_enemy=self.bird.getPos()
        rect_enemy=self.bird.getRect()
        self.player.attackBox.getHit(pos_enemy[0], pos_enemy[1], rect_enemy[0], rect_enemy[1], self.bird)
        #self.player.update()


        if self.bird.getState() == False:  #si es golpeado el candelabro
                item = self.bird.getSpawnedItem()    # se genera un item --retorna un 0?
                iPos = item.getPos()         #Posicion e rect del item
                iRect = item.getRect()

                self.player.passiveBox.getHit(iPos[0], iPos[1], iRect[0], iRect[1], item)

                if item.getState() == False and item.getPickedUpState() == False:
                    item.pickUp()
                    self.player.addHeartToCount(item.getHeartValue())

                for y in self.platformGroup:
                    jPos = y.getPos()
                    jRect = y.getRect()
                    if iPos[0] > jPos[0] and iPos[0] < (jPos[0] + jRect[0]):
                        item.setFloor(jPos[1] + jRect[1] - iRect[1])


        #4
        if self.player.getHeartCount() < 10:
            self.UI_HeartCount.setText("0" + str(self.player.getHeartCount()))
        else:
            self.UI_HeartCount.setText(str(self.player.getHeartCount()))

        self.UI_Time.setText("0" + str(999 - self.runTime))

        self.score = self.player.getHeartCount() * 75
        #5
        if self.score < 10:
            self.UI_Score.setText("00000" + str(self.score))
        elif self.score > 10 and self.score < 100:
            self.UI_Score.setText("0000" + str(self.score))
        elif self.score > 100 and self.score < 1000:
            self.UI_Score.setText("000" + str(self.score))
        elif self.score > 1000:
            self.UI_Score.setText("00" + str(self.score))

        #6
        for x in self.UI_TextGroup:
            x.update()

    def State_Manager(self):
        if self.level == "level_1":
            self.main_game(self.candleGroup_1,self.platformGroup_1)
        if self.level == "level_2":
            self.main_game(self.candleGroup_2,self.platformGroup_2)

    def get_score(self):
        return self.score


