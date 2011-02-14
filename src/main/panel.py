# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import random

import settings
from pywaz.sprite.animation import Animation, AnimationInfo


class Panel(Animation):
    animation_enable = False
    disable = False
    
    def __init__(self, x=0, y=0, owner=0):
        u"""
            x,y: マップ上の相対座標
        """
        super(Panel,self).__init__("../resources/image/main/panel/panels.png",AnimationInfo(0,0,4,20,20,0),x=x*settings.PANELSIZE, y=y*settings.PANELSIZE)
        self.color = random.randint(0,3)
        self.owner = owner
        self.ainfo.index = owner
        self.ainfo.frame = self.color