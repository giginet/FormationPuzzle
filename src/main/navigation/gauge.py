# -*- coding: utf-8 -*-
#
#    Created on 2011/02/26
#    Created by giginet
#
import settings
from pywaz.sprite.image import Image
from pywaz.sprite import OrderedUpdates
from pywaz.core.game import Game
from main.navigation.number import Number

class Gauge(object):
    GAUGE_HEIGHT = 275
    
    def __init__(self,x=0, y=0):
        self.x = x
        self.y = y
        self.gauges = OrderedUpdates(
                                    Image(u'../resources/image/main/navigation/gauge1_half.png', x=self.x, y=self.y+self.GAUGE_HEIGHT),
                                    Image(u'../resources/image/main/navigation/gauge2_half.png', x=self.x, y=self.y)
                                    )
        self.numbers = OrderedUpdates(
                        Number(50, u'../resources/image/main/navigation/number1.png', x=self.x+28, y=self.y+482),
                        Number(50, u'../resources/image/main/navigation/number2.png', x=self.x+28, y=self.y+28)
                        )
        
    def update(self, count):
        u"""
            count tuple
        """
        for i, number in enumerate(self.numbers):
            number.n = int(round(count[i]*100/(settings.STAGE_WIDTH*settings.STAGE_HEIGHT)))
        
    def draw(self):
        rects = []
        #rects = self.gauges.draw(Game.get_screen())
        #rects += self.numbers.draw(Game.get_screen())
        return rects