# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#
from . import Unit
from main.utils import LocalPoint
from parameter import SWEEP

class Sweep(Unit):
    offset = (-1, -1)
    parameter = SWEEP
    
    @classmethod
    def generate(cls, panel, stage):
        point =panel.point
        panels = [panel, stage.get_panel(point+LocalPoint(1,1)),stage.get_panel(point+LocalPoint(-1,1)),stage.get_panel(point+LocalPoint(1,-1)),stage.get_panel(point+LocalPoint(-1,-1))]
        if cls.check(panels):
            for panel in panels: panel.unit = True
            return Sweep(panels)
        return None
