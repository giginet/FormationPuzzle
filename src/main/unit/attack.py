# -*- coding: utf-8 -*-
#
#    Created on 2011/02/17
#    Created by giginet
#
from . import Unit
from main.utils import LocalPoint

class Attack(Unit):
    filepath = u"../resources/image/main/unit/attack.png"
    offset = (-1, -1)
    
    @classmethod
    def generate(cls, panel, stage):
        point =panel.point
        panels = [panel, stage.get_panel(point+LocalPoint(1,0)),stage.get_panel(point+LocalPoint(-1,0)),stage.get_panel(point+LocalPoint(0,1)),stage.get_panel(point+LocalPoint(0,-1))]
        if cls.check(panels):
            return Attack(panels)
        return None