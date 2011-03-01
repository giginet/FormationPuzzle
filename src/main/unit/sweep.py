# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#
import settings

from . import Unit
from main.utils import LocalPoint
from main.panel import DummyPanel
from parameter import SWEEP

class Sweep(Unit):
    offset = (-1, -1)
    parameter = SWEEP
    name = 'sweep'
    
    def __init__(self, panels, stage):
        super(Sweep, self).__init__(panels, stage)
        x = panels[0].point.x
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
            return Sweep(panels, stage)
        return None
    
    def move(self, panels):
        for panel in self.panels:
            owner = panel.owner
            v = LocalPoint(0,1-2*owner)
            p = self.stage.get_panel(panel.point+v)
            while not isinstance(p, DummyPanel):
                if p.owner != owner: p.change_owner(owner)
                p = self.stage.get_panel(p.point+v)
