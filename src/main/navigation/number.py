# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#

from pywaz.sprite.image import Image


import numbers

from pygame.rect import Rect

class Number(object):
    WIDTH = 20
    HEIGHT = 40
    OFFSET = 3
    
    def __init__(self, n, filepath=u'../resources/image/main/navigation/number1.png', x=0, y=0):
        self.n = int(n)
        self.pre_n = self.n
        self.images = []
        self.x = x
        self.y = y
        self.filepath = filepath
        for i,s in enumerate(str(self.n)):
            self.images.append(self._parse(i, int(s)))
        
    def _parse(self, n, i):
        area = Rect(i*self.WIDTH, 0, self.WIDTH, self.HEIGHT)
        return Image(self.filepath,area=area,x=self.x+(self.WIDTH+self.OFFSET)*n,y=self.y)
    
    def render(self):
        if self.n != self.pre_n:
            self.pre_n = self.n
            self.images = []
            for i,s in enumerate(str(self.n)):
                self.images.append(self._parse(i, int(s)))
        for image in self.images:
            image.render()