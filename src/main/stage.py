# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings

from pywaz.utils.singleton import Singleton
from pywaz.sprite.image import Image

from main.player import Player
from main.panel import Panel, PanelSet, DummyPanel

from main.utils import LocalPoint
from main.unit.attack import Attack

class Stage(Singleton):
    frame = Image(u'../resources/image/main/frame.png', x=settings.STAGE_OFFSET[0]-15, y=settings.STAGE_OFFSET[1]-15)
    players = [Player(0)]
    panelsets = [] #回転中のPanelSet
    units = []
    
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
        self._map = map(list, zip(*self._map)) #transpose matrix
        
    def act(self):
        for player in self.players:
            player.act()
            press = player.poll()
            if press:
                lp = player.get_local_point()
                panels = (self.get_panel(lp),self.get_panel(lp+LocalPoint(1,0)),self.get_panel(lp+LocalPoint(1,1)),self.get_panel(lp+LocalPoint(0,1)))
                if self.can_rotation(panels):
                    self.panelsets.append(PanelSet(panels, press))
        for i,ps in enumerate(self.panelsets):
            if ps.is_over():
                self.rotate(ps.panels, ps.degree)
                for panel in ps.panels: 
                    panel.rotation = False
                    self.check(panel)
                del self.panelsets[i]
        map(lambda panelset: panelset.act(),self.panelsets)
        for unit in self.units:
            self.move_unit(unit, LocalPoint(0,-1))
                
    def render(self):
        self.frame.render()
        map((lambda column: map((lambda panel: panel.render()),column)), self._map)
        map(lambda p:p.render(),self.players)
        map(lambda u:u.render(),self.units)
        
    def get_panel(self, lp):
        if 0 <= lp.x < settings.STAGE_WIDTH and 0<= lp.y < settings.STAGE_HEIGHT:
            return self._map[lp.x][lp.y]
        return DummyPanel(lp.x,lp.y)
        
    def swap(self, a, b):
        tmp = a.point
        self._map[a.point.x][a.point.y] = b
        self._map[b.point.x][b.point.y] = a
        a.point = b.point
        b.point = tmp
        
    def rotate(self, panels, degree):
        if degree == 1:
            self.swap(panels[0], panels[3])
            self.swap(panels[3], panels[2])
            self.swap(panels[2], panels[1])
        else:
            self.swap(panels[0], panels[1])
            self.swap(panels[1], panels[2])
            self.swap(panels[2], panels[3])
        for panel in panels: panel.angle = 0
    
    def move_unit(self, unit, vector):
        u"""unitをvectorの方向に移動させる"""
        for panel in unit.panels:
            next = self.get_panel(panel.point+vector)
            if not next.can_through() and not unit.has(next): return
        updates = []
        outdates = []
        for panel in unit.panels:
            updates.append((panel, panel.point+vector))
            self._map[panel.point.x][panel.point.y] = DummyPanel(panel.point.x, panel.point.y)
        for tuple in updates:
            panel = tuple[0]
            to = tuple[1]
            next = self.get_panel(to)
            if not next.unit:
                outdates.append(next)
            self._map[to.x][to.y] = panel
            panel.point = to
        for panel in outdates:
            reverse = vector.clone().reverse()
            current_point = panel.point+reverse
            current_panel = self.get_panel(current_point)
            while current_panel.unit:
                current_point = current_point + reverse
                current_panel = self.get_panel(current_point)
            self._map[current_point.x][current_point.y] = panel
            panel.point = current_point
        
    def can_rotation(self, panels):
        owner = panels[0].owner
        for panel in panels:
            if not panel.can_rotate(): return False
            if panel.owner != owner: return False
        return True
    
    def check(self, panel):
        lp = panel.point
        for x in xrange(lp.x-2,lp.x+2):
            for y in xrange(lp.y-2,lp.y+2):
                unit = Attack.generate(self.get_panel(LocalPoint(x,y)), self)
                if unit: self.units.append(unit)
