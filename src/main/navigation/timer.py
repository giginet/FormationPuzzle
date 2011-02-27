# -*- coding: utf-8 -*-
#
#    Created on 2011/02/24
#    Created by giginet
#
import settings

from pywaz.core.game import Game
from pywaz.utils.timer import Timer as _Timer
from .number import Number
from pywaz.sprite import OrderedUpdates

class Timer(object):
    COLON_HEIGHT = 4
    HEIGHT = 40
    OFFSET = 10
    u"""9分59秒〜0分00秒の間のみ"""
    def __init__(self, max, x=0, y=0):
        self.images = OrderedUpdates()
        self.x = x
        self.y = y
        self.timer = _Timer(max*settings.FRAMERATE)
        self.pre_second = 0
    
    def draw(self):
        rects = self.images.draw(Game.get_screen())
        print reduce(lambda a, b: a+b, rects, [])
        return []
    
    def update(self):
        self.timer.tick()
        n = (self.timer.max - self.timer.now)/settings.FRAMERATE
        minute = int(n/60)
        second = n%60
        if not second == self.pre_second:
            self.images.empty()
            self.images.add(Number(minute,u'../resources/image/main/navigation/time.png', x=self.x, y=self.y))
            self.pre_second = second
            if second < 10:
                self.images.add(Number(0,u'../resources/image/main/navigation/time.png', 
                                       x=self.x, y=self.y+self.HEIGHT+self.COLON_HEIGHT+self.OFFSET*2))
                self.images.add(Number(second,u'../resources/image/main/navigation/time.png', 
                                       x=self.x, y=self.y+self.HEIGHT*2+self.COLON_HEIGHT+self.OFFSET*3))
            else:
                print int(second/10)
                print second%10
                print "-----------"
                self.images.add(Number(int(second/10),u'../resources/image/main/navigation/time.png', 
                                       x=self.x, y=self.y+self.HEIGHT+self.COLON_HEIGHT+self.OFFSET*2))
                self.images.add(Number(second%10,u'../resources/image/main/navigation/time.png', 
                                       x=self.x, y=self.y+self.HEIGHT*2+self.COLON_HEIGHT+self.OFFSET*3))
                    
    def play(self):
        self.timer.play()
        