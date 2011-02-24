# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings

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
        self.sprites.add(self.background)
        self.stage = Stage()
        self.bgm = BGM(u'../resources/bgm/game_intro.wav', -1, u'../resources/bgm/game_loop.wav')
        self.timer = NavigationTimer(120, x=100, y=100)
        self.timer.play()
        
    def update(self):
        super(GameScene, self).update()
        self.stage.update()
        self.bgm.play()
        self.timer.update()
    
    def draw(self):
        rect_draw = super(GameScene, self).draw()
        rect_draw += self.stage.draw()
        self.timer.draw()
        return rect_draw