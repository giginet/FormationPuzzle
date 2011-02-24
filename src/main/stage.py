# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings

from pywaz.utils.singleton import Singleton
from pywaz.sprite.image import Image
from pywaz.core.game import Game

from main.player import Player, NPC
from main.panel import Panel, PanelSet, DummyPanel

from main.utils import LocalPoint
from main.unitmanager import UnitManager

class Stage(Singleton):
    frame = Image(u'../resources/image/main/frame.png', x=settings.STAGE_OFFSET[0]-15, y=settings.STAGE_OFFSET[1]-15)
    players = [Player(0), Player(1)]
    panelsets = [] #回転中のPanelSet
    
    def __init__(self):
        game = Game()
        game.add(self.frame)
        self._map = []
        self.unitmng = UnitManager(self)
        for y in xrange(settings.STAGE_HEIGHT):
            column = []
            for x in xrange(settings.STAGE_WIDTH):
                owner = 0
                if y < settings.STAGE_HEIGHT/2:
                    owner = 1
                panel = Panel(x, y, owner)
                column.append(panel)
                game.add(panel)
            self._map.append(column)
        self._map = map(list, zip(*self._map)) #transpose matrix
        for p in self.players:
            game.add(p)
        
    def update(self):
        for player in self.players:
            player.update()
            press = player.poll()
            if press:
                lp = player.get_local_point()
                panels = (self.get_panel(lp),self.get_panel(lp+LocalPoint(1,0)),self.get_panel(lp+LocalPoint(1,1)),self.get_panel(lp+LocalPoint(0,1)))
                for p in panels:
                    if p.unit:
                        self.unitmng.remove(self.unitmng.get_unit_by_panel(p))
                        break
                if self.can_rotation(panels):
                    self.panelsets.append(PanelSet(panels, press))
        for i,ps in enumerate(self.panelsets):
            if ps.is_over():
                self.rotate(ps.panels, ps.degree)
                for panel in ps.panels: 
                    panel.rotation = False
                    self.unitmng.check(panel)
                del self.panelsets[i]
        map(lambda panelset: panelset.update(),self.panelsets)
        for unit in self.unitmng.units:
            res = unit.update()
            if res == -1:
                self.unitmng.remove(unit)
            elif res:
                vector = unit.degree
                enemies = []
                hit = False
                for panel in unit.panels:
                    next = self.get_panel(panel.point+vector)
                    if not next.can_through() and not unit.has(next):
                        hit = True
                        neighbor_unit = self.unitmng.get_unit_by_panel(next) 
                        if not next.is_dummy() and neighbor_unit and not neighbor_unit in enemies and not neighbor_unit.owner == unit.owner:
                            enemies.append(neighbor_unit)
                if enemies:
                    map(lambda enemy: self.unitmng.battle(unit, enemy), enemies)
                elif not hit:
                    self.unitmng.move_unit(unit, vector)
    def draw(self):
        rect_draw = []
        self.frame.draw()
        #map((lambda column: map((lambda panel: panel.draw()),column)), self._map)
        map(lambda u:u.draw(),self.unitmng.units)
        #map(lambda p:p.draw(),self.players)
        return rect_draw
        
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
    
    def can_rotation(self, panels):
        owner = panels[0].owner
        for panel in panels:
            if not panel.can_rotate(): return False
            if panel.owner != owner: return False
        return True
    
    def culc_gauge(self):
        count = [0,0]
        for x in xrange(settings.STAGE_WIDTH):
            for y in xrange(settings.STAGE_HEIGHT):
                count[self._map[x][y].owner]+=1
        return count