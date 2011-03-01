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
        p = panels[0]
        distances = [0,0]
        edge = [False, False]
        for i,v in enumerate([LocalPoint(-1, 0), LocalPoint(1,0)]):
            d = 0
            next_point = p.point + v
            while True:
                next_point += v
                next = self.stage.get_panel(next_point)
                d +=1
                if isinstance(next, DummyPanel):
                    edge[i] = True
                    distances[i] = d
                    break
                elif not next.owner == p.owner:
                    edge[i] = False
                    distances[i] = d
                    break
        if edge[0] and edge[1]:
            u"""両方とも端まで行った場合は遠い方を採用"""
            x = p.point.x
            if distances[0] < distances[1]:
                self.degree = LocalPoint(1,0)
            else:
                self.degree = LocalPoint(-1,0)
        else:
            u"""どちらかで敵パネルを見つけたときは、敵パネルがあって近い方"""
            if edge[0] and not edge[1]:
                self.degree = LocalPoint(1,0)
            elif not edge[0] and edge[1]:
                self.degree = LocalPoint(-1,0)
            else:
                if distances[0] < distances[1]:
                    self.degree = LocalPoint(-1,0)
                else:
                    self.degree = LocalPoint(1,0)
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
                if p.owner != owner: 
                    p.change_owner(owner)
                    p.set_disable(True)
                p = self.stage.get_panel(p.point+v)
