# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings

from pywaz.utils.singleton import Singleton
from pywaz.sprite.image import Image

from main.player import Player
from main.panel import Panel, PanelSet

from main.utils import LocalPoint

class Stage(Singleton):
    frame = Image(u'../resources/image/main/frame.png', x=settings.STAGE_OFFSET[0]-15, y=settings.STAGE_OFFSET[1]-15)
    players = [Player(0)]
    panelsets = [] #回転中のPanelSet
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
        self._map = map(list, zip(*self._map))
        
    def act(self):
        for player in self.players:
            player.act()
            press = player.poll()
            if press:
                lp = player.get_local_point()
                panels = (self.get_panel(lp),self.get_panel(lp+LocalPoint(1,0)),self.get_panel(lp+LocalPoint(1,1)),self.get_panel(lp+LocalPoint(0,1)))
                self.panelsets.append(PanelSet(panels, press))        
        map(lambda panelset: panelset.act(),self.panelsets)
                
    def render(self):
        self.frame.render()
        map((lambda column: map((lambda panel: panel.render()),column)), self._map)
        map(lambda p:p.render(),self.players)
        
    def get_panel(self, lp):
        return self._map[lp.x][lp.y]