# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings

from pywaz.utils.singleton import Singleton
from pywaz.sprite.image import Image

from main.player import Player
from main.panel import Panel

class Stage(Singleton):
    frame = Image(u'../resources/image/main/frame.png', x=settings.STAGE_OFFSET[0]-15, y=settings.STAGE_OFFSET[1]-15)
    players = [Player(0), Player(1)]
    
    def __init__(self):
        self._map = []
        for y in xrange(settings.STAGE_HEIGHT):
            column = []
            for x in xrange(settings.STAGE_WIDTH):
                owner = 0
                if y < settings.STAGE_HEIGHT/2:
                    owner = 1
                column.append(Panel(x, y, owner))
            self._map.append(column)
        
    def act(self):
        self.players[0].act()
    
    def render(self):
        self.frame.render()
        map((lambda column: map((lambda panel: panel.render()),column)), self._map)
        self.players[0].render()
        
    def get_panel(self, x, y):
        return self._map[x][y]