# -*- coding: utf-8 -*-
#
#    Created on 2011/02/17
#    Created by giginet
#
import pygame
import settings

from pywaz.sprite.animation import Image
from pywaz.device.mouse import Mouse
from pywaz.device.key import Key

from main.utils import global_to_local, LocalPoint, local_to_global

class Player(Image):
    is_human = True
    pressed = False
    initial_position = (
                        (settings.STAGE_WIDTH-1, settings.STAGE_HEIGHT-1),
                        (0,0),
    )
    
    def __init__(self, n):
        self.number = n
        self.x, self.y = local_to_global(self.initial_position[n]).to_pos()
        self.point = LocalPoint(0,0)
        super(Player, self).__init__(u'../resources/image/main/player/cursor.png', area=pygame.rect.Rect(0,n*40,40,40),x=100, y=100)
        self.animation_enable = False
        
    def update(self):
        if self.number == 0:
            if self.in_map():
                self.x, self.y = map((lambda x: x-settings.PANELSIZE),(self.get_local_point().add(LocalPoint(1,1))).to_global().to_pos())
                self.rect.x = self.x
                self.rect.y = self.y
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
    
class NPC(Player):
    pass