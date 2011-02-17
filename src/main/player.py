# -*- coding: utf-8 -*-
#
#    Created on 2011/02/17
#    Created by giginet
#
import settings
from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.device.mouse import Mouse

from main.utils import global_to_local, LocalPoint

class Player(Animation):
    is_human = True
    def __init__(self, n, human=True):
        self.number = n
        self.is_human = human
        super(Player, self).__init__(u'../resources/image/main/player/cursorA.png', AnimationInfo(0,0,0,40,40,0))
        self.ainfo = AnimationInfo(0,0,0,40,40,0)
        self.animation_enable = False
        #Mouse.hide_cursor()
        
    def act(self):
        self.x, self.y = map((lambda x: x-settings.PANELSIZE),(global_to_local(Mouse.get_pos()).add(LocalPoint(1,1))).to_global().to_pos())

class NPC(Animation):
    pass