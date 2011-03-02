# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#
from . import Unit
from main.utils import LocalPoint
from settings.parameter import GUARD

class Guard(Unit):
    offset = (-1, 0)
    parameter = GUARD
    name = 'guard'
    
    @classmethod
    def generate(cls, panel, stage):
        point =panel.point
        panels = [panel, stage.get_panel(point+LocalPoint(1,0)),stage.get_panel(point+LocalPoint(2,0)),stage.get_panel(point+LocalPoint(-1,0))]
        if cls.check(panels):
            for panel in panels: panel.unit = True
            return Guard(panels, stage)
        return None