# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#
import settings

from . import Unit
from main.utils import LocalPoint
from parameter import SWEEP

class Sweep(Unit):
    offset = (-1, -1)
    parameter = SWEEP
    
    def __init__(self, panels):
        super(Sweep, self).__init__(panels)
        x = panels[0].point.x
        print cmp(x,settings.STAGE_WIDTH-x)
        if cmp(x,settings.STAGE_WIDTH-x) < 0:
            self.degree = LocalPoint(1,0)
        else:
            self.degree = LocalPoint(-1,0)
    @classmethod
    def generate(cls, panel, stage):
        point =panel.point
        panels = [panel, stage.get_panel(point+LocalPoint(1,1)),stage.get_panel(point+LocalPoint(-1,1)),stage.get_panel(point+LocalPoint(1,-1)),stage.get_panel(point+LocalPoint(-1,-1))]
        if cls.check(panels):
            for panel in panels: panel.unit = True
            return Sweep(panels)
        return None
