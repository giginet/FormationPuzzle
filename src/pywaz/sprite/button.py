# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
from animation import Animation, AnimationInfo
from ..device.mouse import Mouse

class Button(Animation):
    pressed = False
    hovered = False
    animation_enable = False
    
    def __init__(self, filepath, x=0, y=0, w=0, h=0):
        super(Button, self).__init__(filepath, AnimationInfo(0,0,1,w,h), x=x, y=y)
    
    def on_mouseout(self):
        self.ainfo.index = 0
    
    def on_mouseover(self):
        self.ainfo.index = 1
    
    def on_press(self):
        self.ainfo.index = 2
    
    def on_release(self):
        self.ainfo.index = 3
    
    def update(self):
        if self.hit_area.collidepoint(Mouse.get_pos()):
            if not self.hovered:
                self.on_mouseover()
            self.hovered = True
            if Mouse.is_press('LEFT'):
                self.pressed = True
            else:
                self.pressed = False
        else:
            if self.pressed:
                self.on_release()
            if self.hovered:
                self.mouseout()
            self.pressed = False
            self.hovered = False