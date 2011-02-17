# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import random

import settings
from pywaz.sprite.image import Image
from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.utils.vector import Vector
from pywaz.utils.timer import Timer

from main.utils import LocalPoint

class Panel(Image):
    disable = False
    
    def __init__(self, x=0, y=0, owner=0):
        u"""
            x,y: マップ上の相対座標
        """
        self.point = LocalPoint(x,y)
        self.color = random.randint(0,3)
        self.owner = owner 
        super(Panel,self).__init__("../resources/image/main/panel/panel%d_%d.png" % (owner, self.color), x=x*settings.PANELSIZE+settings.STAGE_OFFSET[0], y=y*settings.PANELSIZE+settings.STAGE_OFFSET[1])
        
    def render(self):
        super(Panel, self).render()
        
class PanelSet(object):
    def __init__(self, panels, degree=0):
        u"""
            panels    左上から時計回りに4枚のパネルを渡す
            degree    回転方向を渡す。1なら反時計回り、-1なら時計回り
        """
        self.degree = degree
        self.panels = panels
        self.timer = Timer(10)
        panels[0].center = Vector(settings.PANELSIZE,settings.PANELSIZE)
        panels[1].center = Vector(0, settings.PANELSIZE)
        panels[2].center = Vector(0,0)
        panels[3].center = Vector(settings.PANELSIZE,0)
        self.timer.play()
        
    def act(self):
        self.timer.tick()
        if not self.timer.is_over():
            for panel in self.panels:
                panel.angle = self.timer.now*90/self.timer.max*self.degree
        else:
            for panel in self.panels:
                panel.angle = 90*self.degree