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

from main.utils import global_to_local, LocalPoint, local_to_global

class Player(Animation):
    is_human = True
    pressed = False
    initial_position = (
                        (settings.STAGE_WIDTH-1, settings.STAGE_HEIGHT-1),
                        (0,0),
    )
    
    
    def __init__(self, n):
        self.number = n
        super(Player, self).__init__(u'../resources/image/main/player/cursor.png', AnimationInfo(n,0,0,40,40,0))
        self.animation_enable = False
        Mouse.hide_cursor()
        self.x, self.y = local_to_global(self.initial_position[n]).to_pos()
        
    def update(self):
        if self.number == 0:
            if self.in_map():
                self.x, self.y = map((lambda x: x-settings.PANELSIZE),(self.get_local_point().add(LocalPoint(1,1))).to_global().to_pos())
                Mouse.hide_cursor()
            else: 
                Mouse.show_cursor()
        
    def poll(self):
        if self.number == 0:
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
    
    def in_map(self):
        lp = self.get_local_point()
        return 0 <= lp.x < settings.STAGE_WIDTH-1 and 0 <= lp.y < settings.STAGE_HEIGHT-1

class NPC(Animation):
    pass