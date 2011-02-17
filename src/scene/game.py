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

class GameScene(Scene):
    def ready(self):
        self.stage = Stage()
        
    def act(self):
        self.stage.act()
    
    def render(self):
        super(GameScene, self).render()
        self.stage.render()