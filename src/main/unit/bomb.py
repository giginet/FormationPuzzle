# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#
from . import Unit
from main.utils import LocalPoint
from parameter import BOMB

class Bomb(Unit):
    offset = (0, 0)
    parameter = BOMB
    name = 'bomb'
    
    @classmethod
    def generate(cls, panel, stage):
        point =panel.point
        panels = [panel, stage.get_panel(point+LocalPoint(1,0)),stage.get_panel(point+LocalPoint(1,1)),stage.get_panel(point+LocalPoint(0,1))]
        if cls.check(panels):
            for panel in panels: panel.unit = True
            return Bomb(panels, stage)
        return None
    
    def disappear(self):
        owner = self.panels[0].owner
        for i, player in enumerate(self.stage.players):
            if i != owner:
                lp = player.get_local_point()
                break
        self.stage.get_panel(lp).set_disable(True)
        self.stage.get_panel(lp+LocalPoint(0,1)).set_disable(True)
        self.stage.get_panel(lp+LocalPoint(1,1)).set_disable(True)
        self.stage.get_panel(lp+LocalPoint(1,0)).set_disable(True)
        super(Bomb, self).disappear()