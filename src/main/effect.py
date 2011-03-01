# -*- coding: utf-8 -*-
#
#    Created on 2011/03/01
#    Created by giginet
#
from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.sprite import OrderedUpdates

class Effect(Animation):
    effects = OrderedUpdates()
    
    def __init__(self, filepath, ainfo, x=0, y=0):
        super(Effect, self).__init__(filepath, ainfo, x, y)
        self.effects.add(self)
    
    def update(self):
        super(Effect, self).update()
        if self.is_over():
            self.effects.remove(self)