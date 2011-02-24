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
        self.stage = Stage()
        self.background = Image(u'../resources/image/main/background.png')
        self.bgm = BGM(u'../resources/bgm/game_intro.wav', -1, u'../resources/bgm/game_loop.wav')
        self.sprites.append(self.background)
        self.timer = NavigationTimer(120, x=100, y=100)
        self.timer.play()
        
    def act(self):
        self.stage.act()
        self.bgm.play()
        self.timer.act()
    
    def render(self):
        super(GameScene, self).render()
        self.stage.render()
        self.timer.render()