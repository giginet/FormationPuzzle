# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings

from pywaz.utils.singleton import Singleton
from main.panel import Panel

class Stage(Singleton):
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
        pass
    
    def render(self):
        map((lambda column: map((lambda panel: panel.render()),column)), self._map)
        
    def get_panel(self, x, y):
        return self._map[x][y]