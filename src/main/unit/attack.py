# -*- coding: utf-8 -*-
#
#    Created on 2011/02/17
#    Created by giginet
#
from . import Unit
from main.utils import LocalPoint
from parameter import ATTACK

class Attack(Unit):
    offset = (-1, -1)
    parameter = ATTACK
    name = 'attack'
        
    @classmethod
    def generate(cls, panel, stage):
        point =panel.point
        panels = [panel, stage.get_panel(point+LocalPoint(1,0)),stage.get_panel(point+LocalPoint(-1,0)),stage.get_panel(point+LocalPoint(0,1)),stage.get_panel(point+LocalPoint(0,-1))]
        if cls.check(panels):
            for panel in panels: panel.unit = True
            return Attack(panels, stage)
        return None