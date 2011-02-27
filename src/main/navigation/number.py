# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#

from pywaz.sprite.image import Image


import numbers

from pygame.rect import Rect
from pygame.sprite import Sprite
from pywaz.sprite import OrderedUpdates
from pywaz.core.game import Game

class Number(Sprite):
    WIDTH = 20
    HEIGHT = 40
    OFFSET = 3
    
    def __init__(self, n, filepath=u'../resources/image/main/navigation/number1.png', x=0, y=0):
        super(Number, self).__init__()
        self.n = int(n)
        self.pre_n = self.n
        self.images = OrderedUpdates()
        self.x = x
        self.y = y
        self.filepath = filepath
        self._parse()
        
    def _parse(self):
        self.images.empty()
        for i,s in enumerate(str(self.n)):
            n = int(s)
            area = Rect(n*self.WIDTH, 0, self.WIDTH, self.HEIGHT)
            self.images.add(Image(self.filepath,area=area,x=self.x+(self.WIDTH+self.OFFSET)*i,y=self.y))
    
    def draw(self, surface):
        if self.n != self.pre_n:
            self.pre_n = self.n
            self._parse()
        return self.images.draw(Game.get_screen())