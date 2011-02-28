# -*- coding: utf-8 -*-
#
#    Created on 2011/02/26
#    Created by giginet
#
import settings
import pygame
from pywaz.sprite.image import Image
from pywaz.sprite import OrderedUpdates
from pywaz.core.game import Game
from pywaz.utils.vector import Vector
from main.navigation.number import Number

class Gauge(object):
    GAUGE_HEIGHT = 275
    CHIPS = settings.STAGE_WIDTH*settings.STAGE_HEIGHT
    OFFSET = ((0,0),(28,482),(28,28))
    
    def __init__(self,x=0, y=0):
        self.x = x
        self.y = y
        self.gauges = (
                        Image(u'../resources/image/main/navigation/gauge1_full.png'),
                        Image(u'../resources/image/main/navigation/gauge2_half.png')
                      )
        self.gauges[0].center = Vector(0, self.gauges[0].rect.h)
        self.gauges[1].center = Vector(0, 0)
        self.numbers = (
                        Number(50, u'../resources/image/main/navigation/number1.png', x=28, y=482),
                        Number(50, u'../resources/image/main/navigation/number2.png', x=28, y=28)
                        )
        number_size = self.numbers[0].get_surface().get_size()
        self.images = (pygame.surface.Surface((25,self.GAUGE_HEIGHT*2)),
                       pygame.surface.Surface((number_size[0],number_size[1])),
                       pygame.surface.Surface((number_size[0],number_size[1])),
                       )
        map(lambda image:image.set_colorkey((0,0,0)), self.images)
        self.proportion = [50,50]
        self.pre_proportion = [0,0]

    def update(self, count):
        u"""
            count tuple
        """
        self.proportion[0] = int(count[0]*100/self.CHIPS)
        self.proportion[1] = 100 - int(count[0]*100/self.CHIPS)
        if not self.proportion[0] == self.pre_proportion[0]:
            self.pre_proportion = list(self.proportion)
            self._parse()
        
    def draw(self, surface=Game.get_screen()):
        for sprite, offset in zip(self.images, self.OFFSET):
            rect = sprite.get_rect().move(self.x+offset[0], self.y+offset[1])
            surface.blit(settings.BACKGROUND.image, rect, rect)
        for sprite, offset in zip(self.images, self.OFFSET):
            dest = sprite.get_rect().move(self.x+offset[0], self.y+offset[1])
            surface.blit(sprite, dest)
        return []
        
    def _parse(self):
        for i,gauge in enumerate(self.gauges):
            if i==1: gauge.yscale = float(self.proportion[i])/50
            gauge.draw(self.images[0])
        for i,number in enumerate(self.numbers):
            self.images[i+1].blit(settings.BACKGROUND.image, number.image.get_rect(), 
                                number.image.get_rect())
            number.n = self.proportion[i]
            number.draw(self.images[i+1])
            self.images[i+1].blit(number.get_surface(), number.get_surface().get_rect())