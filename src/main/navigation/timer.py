# -*- coding: utf-8 -*-
#
#    Created on 2011/02/24
#    Created by giginet
#
import settings
import pygame

from pywaz.core.game import Game
from pywaz.utils.timer import Timer as _Timer
from .number import Number
from pygame.sprite import OrderedUpdates
from pywaz.sprite.image import Image
from pywaz.utils.vector import Vector

class Timer(pygame.sprite.Sprite):
    COLON_HEIGHT = 4
    HEIGHT = 40
    WIDTH = 20
    OFFSET = 10
    u"""9分59秒〜0分00秒の間のみ"""
    def __init__(self, max, x=0, y=0):
        super(Timer, self).__init__()
        self.x = x
        self.y = y
        self.timer = _Timer(max*settings.FRAMERATE)
        self.gauge = Image(u'../resources/image/main/navigation/gauge_timer.png')
        self.gauge.center = Vector(0, self.gauge.rect.h)
        self.pre_second = 0
        self.image = pygame.surface.Surface((70,396)).convert()
        self.image.set_colorkey((0,0,0))
        self._parse(self.convert_time())
    
    def draw(self, surface=Game.get_screen()):
        surface.blit(self.image, self.image.get_rect().move(self.x, self.y))
        return []
        
    def _parse(self, time):
        minute = time[0]
        second = time[1]
        minute_surface = Number(minute, u'../resources/image/main/navigation/time.png').get_surface()
        timer_surface = pygame.surface.Surface((self.WIDTH,self.HEIGHT*3+self.COLON_HEIGHT+self.OFFSET*3))
        timer_surface.blit(minute_surface, minute_surface.get_rect())
        self.pre_second = second
        if second < 10:
            second10 = Number(0,u'../resources/image/main/navigation/time.png').get_surface()
            second1 = Number(second,u'../resources/image/main/navigation/time.png').get_surface()
        else:
            second10 = Number(int(second/10),u'../resources/image/main/navigation/time.png').get_surface()
            second1 = Number(second%10,u'../resources/image/main/navigation/time.png').get_surface()
        timer_surface.blit(second10, second10.get_rect().move(0, self.HEIGHT+self.COLON_HEIGHT+self.OFFSET*2))
        timer_surface.blit(second1, second1.get_rect().move(0, self.HEIGHT*2+self.COLON_HEIGHT+self.OFFSET*3))
        self.image.blit(settings.BACKGROUND.image, self.gauge.image.get_rect(), self.gauge.image.get_rect().move(self.x, self.y))
        self.image.blit(timer_surface, timer_surface.get_rect().move(28,96))
        self.gauge.yscale = float(self.timer.max-self.timer.now)/float(self.timer.max)
        self.gauge.draw(self.image)
        
    def update(self):
        self.timer.tick()
        second = self.convert_time()[1]
        if not second == self.pre_second:
            self._parse(self.convert_time())        
    def play(self):
        self.timer.play()
    
    def convert_time(self):
        n = (self.timer.max - self.timer.now)/settings.FRAMERATE
        return int(n/60), n%60    
    
    def is_over(self):
        return self.timer.is_over()