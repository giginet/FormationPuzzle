# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
from pywaz.scene.abstractscene import Scene
from pywaz.core.game import Game
from pywaz.sprite.image import Image
from pywaz.mixer.bgm import BGM
from pywaz.utils.vector import Vector
from pywaz.utils.timer import Timer
from pywaz.device.mouse import Mouse

class MainScene(Scene):
    def ready(self):
        i = Image(u"../resources/image/main/panel/panel.png", x=100, y=100)
        i.center = Vector(0,0)
        self.sprites.append(i)
        
    def act(self):
        for kawaz in self.sprites:
            kawaz.angle +=1