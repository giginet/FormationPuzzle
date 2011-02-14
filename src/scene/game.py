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

from main.panel import Panel
from main.stage import Stage

class GameScene(Scene):
    def ready(self):
        panels = []
        for i in xrange(settings.STAGE_WIDTH*settings.STAGE_HEIGHT):
            p = Panel(i%settings.STAGE_WIDTH,int(i/settings.STAGE_WIDTH))
            self.sprites.append(p)
        
    def act(self):
        pass
        #for kawaz in self.sprites:
        #    kawaz.angle +=1