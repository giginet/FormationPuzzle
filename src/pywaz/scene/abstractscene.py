# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
class Scene(object):
    key = u"AbstractScene"
    BACKGROUND = (0,0,0)
    
    def __init__(self):
        self.sprites = []
    
    def ready(self):
        raise NotImplementedError
    
    def act(self):
        raise NotImplementedError
    
    def render(self):
        for sprite in self.sprites:
            sprite.render()
    
    def finalize(self):
        self.sprites = []