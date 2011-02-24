# -*- coding: utf-8 -*-
#
#    Created on 2011/02/24
#    Created by giginet
#
import settings

from pywaz.utils.timer import Timer as _Timer
from .number import Number
from pywaz.sprite.animation import Animation, AnimationInfo, Image

class Timer(object):
    COLON_HEIGHT = 4
    HEIGHT = 40
    OFFSET = 10
    u"""9分59秒〜0分00秒の間のみ"""
    def __init__(self, max, x=0, y=0):
        self.images = [None,None,None,None]
        self.x = x
        self.y = y
        self.images[1] = Image(u'../resources/image/main/navigation/colon.png',x=self.x, y=self.y+self.HEIGHT+self.OFFSET)
        self.timer = _Timer(max*settings.FRAMERATE)
        self.pre_second = 0
    
    def render(self):
        for image in self.images:
            if image: image.render()
    
    def act(self):
        self.timer.tick()
        n = (self.timer.max - self.timer.now)/settings.FRAMERATE
        minute = int(n/60)
        second = n%60
        self.images[0] = Number(minute,u'../resources/image/main/navigation/time.png', x=self.x, y=self.y)
        if not second == self.pre_second:
            self.pre_second = second
            if second < 10:
                self.images[2] = Number(0,u'../resources/image/main/navigation/time.png', x=self.x, y=self.x+self.HEIGHT+self.COLON_HEIGHT+self.OFFSET*2)
                self.images[3] = Number(second,u'../resources/image/main/navigation/time.png', x=self.x, y=self.x+self.HEIGHT*2+self.COLON_HEIGHT+self.OFFSET*3)
            else:
                self.images[2] = Number(int(second/10),u'../resources/image/main/navigation/time.png', x=self.x, y=self.x+self.HEIGHT+self.COLON_HEIGHT+self.OFFSET*2)
                self.images[3] = Number(second%10,u'../resources/image/main/navigation/time.png', x=self.x, y=self.x+self.HEIGHT*2+self.COLON_HEIGHT+self.OFFSET*3)
                
    def play(self):
        self.timer.play()
        