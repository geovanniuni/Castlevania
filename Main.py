import pygame, sys
from pygame.locals import *

from Character.Belmont import Belmont
from Props.Candle import Candle
from Collision.Platform import PlatformBox
from Stage.Stage import Stage
from UI.UI import UI_Image
from UI.UI import UI_Text
from GameR.GameState import GameState
from Character.Enemy import Enemy

pygame.init()
fpsLimit = pygame.time.Clock()
runTime = pygame.time.get_ticks()/1000

winWidth = 578
winHeight = 448

win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption('Castlevania Gameplay')

bg = pygame.Color(0,0,0)

player = Belmont()
player.setPos(-10,244)

squelet= Enemy("01",5,40,30,10)
bird=Enemy("02",4,25,25)

monkey=Enemy("03",4,40,30)
knight=Enemy("04",2,30,25)
owl=Enemy("05",3,60,40)


squelet.setMove(True)
squelet.setPos(200,325)
bird.setPos(200,250)

monkey.setPos(100,370)
knight.setPos(250,350)
owl.setPos(200,150)



squelet.setSpeed(1,'x')
bird.setSpeed(2,"x")

knight.setSpeed(3,'x')
knight.setLimits(10,400)
owl.setSpeed(4,"x")

enemyGroup=[squelet,bird,monkey,knight,owl]

candle01_1 = Candle(84, 240)
candle02_1 = Candle(157, 261)
candle03_1 = Candle(243, 244)
candle04_1 = Candle(372, 196)
candle05_1 = Candle(502, 239)

candleGroup_1 = [candle01_1, candle02_1, candle03_1, candle04_1, candle05_1]
#itemGroup = []

#ni idea
currentStage = Stage(0, 80, 4)

platform01_1 = PlatformBox(68, 340, 511, 60)
platform02_1 = PlatformBox(0, 244, 68, 60)
platform03_1 = PlatformBox(522, 213, 56, 60)
platform04_1 = PlatformBox(137, 276, 56, 60)
platform05_1 = PlatformBox(392, 276, 56, 60)

platformGroup_1 = [platform01_1, platform02_1, platform03_1, platform04_1, platform05_1]

candle01_2 = Candle(70, 240)
candle02_2 = Candle(100, 200)
candle03_2 = Candle(200, 250)
candle04_2 = Candle(300, 250)
candle05_2 = Candle(400, 200)

candleGroup_2 = [candle01_2, candle02_2, candle03_2, candle04_2, candle05_2]


platform01_2 = PlatformBox(68, 340, 511, 60)
platform02_2 = PlatformBox(0, 244, 68, 60)
platform03_2 = PlatformBox(522, 213, 56, 60)
platform04_2 = PlatformBox(137, 276, 56, 60)
platform05_2 = PlatformBox(392, 276, 56, 60)

platformGroup_2 = [platform01_2, platform02_2, platform03_2, platform04_2, platform05_2]
score = 0
count= 0

UI_fontSize = 16

UI_Top = UI_Image(0,0,'UI.png')
UI_Score = UI_Text(95, 12, "emulogic.ttf", "000000", UI_fontSize)
UI_Time = UI_Text(286, 12, "emulogic.ttf", "0000", UI_fontSize)
UI_HeartCount = UI_Text(367, 29, "emulogic.ttf", "ASD", UI_fontSize)
UI_LifeCount = UI_Text(367, 45, "emulogic.ttf", "05", UI_fontSize)

UI_TextGroup = [UI_Score, UI_Time, UI_HeartCount, UI_LifeCount]

level="level_1"

while True:
    #windows --> la display
    #fill ---> solid color ---> Me parece innecesario
    #win.fill(bg)

#Este update es del modulo stage -->
    currentStage.update()

    runTime = pygame.time.get_ticks()/1000

    game_state = GameState(level, player,enemyGroup, fpsLimit,candleGroup_1,platformGroup_1,candleGroup_2,platformGroup_2,
                           UI_Top, UI_HeartCount, UI_Time,runTime ,UI_Score, UI_TextGroup, score)
    #game_state_2=GameState()


    if level=="level_1":
        game_state.State_Manager()

        count = game_state.get_score()
        if count > 400:
            level="level_2"
            currentStage = Stage(0, 80, 5)
    else:
        game_state.State_Manager()




#display.update ---> part of it, without arguments all screen
# display.flip ----> update all the screen
    pygame.display.update()
