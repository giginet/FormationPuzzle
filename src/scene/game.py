# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings
import pygame

from pywaz.scene.abstractscene import Scene
from pywaz.core.game import Game
from pywaz.sprite.image import Image
from pywaz.mixer.bgm import BGM
from pywaz.utils.vector import Vector
from pywaz.utils.timer import Timer
from pywaz.device.mouse import Mouse

from main.stage import Stage
from main.navigation.number import Number
from main.navigation.timer import Timer as NavigationTimer

class GameScene(Scene):
    def ready(self):
        self.background = Image(u'../resources/image/main/background.png')
        self.frame = Image(u'../resources/image/main/frame.png', x=settings.STAGE_OFFSET[0]-15, y=settings.STAGE_OFFSET[1]-15)
        self.stage = Stage()
        self.bgm = BGM(u'../resources/bgm/game_intro.wav', -1, u'../resources/bgm/game_loop.wav')
        self.timer = NavigationTimer(120, x=100, y=100)
        self.timer.play()
        self.background.draw()
        self.frame.draw()
        pygame.display.update()
        
    def update(self):
        super(GameScene, self).update()
        self.stage.update()
        #if not settings.DEBUG: 
        self.bgm.play()
        self.timer.update()
    
    def draw(self):
        super(GameScene, self).draw()
        if self.stage.redraw_frame(): self.frame.draw() #マップのはじで回転させたとき、回転の軌跡が残ってしまうため、フレームを再描画
        rect_draw = self.stage.draw()
        self.timer.draw()
        return rect_draw