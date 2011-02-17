# -*- coding: utf-8 -*-
#
#    Created on 2011/02/17
#    Created by giginet
#
import settings
import math

from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.device.mouse import Mouse
from pywaz.utils.timer import Timer

from main.utils import global_to_local, LocalPoint

class Player(Animation):
    is_human = True
    pressed = False
    def __init__(self, n, human=True):
        self.number = n
        self.is_human = human
        super(Player, self).__init__(u'../resources/image/main/player/cursor.png', AnimationInfo(n,0,0,40,40,0))
        self.animation_enable = False
        Mouse.hide_cursor()
        
    def act(self):
        self.x, self.y = map((lambda x: x-settings.PANELSIZE),(global_to_local(Mouse.get_pos()).add(LocalPoint(1,1))).to_global().to_pos())
        
    def poll(self):
        if Mouse.is_press('LEFT') and not self.pressed:
            self.pressed = True
            return 1
        elif Mouse.is_press('RIGHT') and not self.pressed:
            self.pressed = True
            return -1
        if Mouse.is_release(self):
            self.pressed = False
        return 0
    
    def get_local_point(self):
        return global_to_local(Mouse.get_pos())

class NPC(Animation):
    pass