# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings

from pygame.rect import Rect

from pywaz.utils.singleton import Singleton
from pywaz.sprite.image import Image
from pywaz.core.game import Game
from pywaz.sprite import OrderedUpdates

from main.player import Player, NPC
from main.panel import Panel, PanelSet, DummyPanel
from main.effect import Effect

from main.utils import LocalPoint
from main.unitmanager import UnitManager


class Stage(Singleton):
    def __init__(self, bomb=False, cpu=True):
        self.bomb = bomb
        self.cpu = cpu
        self.chips = OrderedUpdates()
        self._map = []
        self.unitmng = UnitManager(self)
        self.unitmng.reset()
        for y in xrange(settings.STAGE_HEIGHT):
            column = []
            for x in xrange(settings.STAGE_WIDTH):
                owner = 0
                if y < settings.STAGE_HEIGHT/2:
                    owner = 1
                panel = Panel(x, y, owner)
                column.append(panel)
                self.chips.add(panel)
            self._map.append(column)
        self._map = map(list, zip(*self._map)) #transpose matrix
        if cpu:
            self.players = OrderedUpdates(Player(0), NPC(1))
        else:
            self.players = OrderedUpdates(Player(0), Player(1))
        self.panelsets = [] #回転中のPanelSet
        self.count = [settings.STAGE_WIDTH*settings.STAGE_HEIGHT/2,settings.STAGE_WIDTH*settings.STAGE_HEIGHT/2]
    
        
    def update(self):
        for player in self.players:
            player.update()
            press = player.poll()
            if press:
                lp = player.point
                panels = (self.get_panel(lp),self.get_panel(lp+LocalPoint(1,0)),self.get_panel(lp+LocalPoint(1,1)),self.get_panel(lp+LocalPoint(0,1)))
                if self.can_rotation(panels, player.number):
                    for p in panels:
                        if p.unit:
                            self.unitmng.remove(self.unitmng.get_unit_by_panel(p))
                            break
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
        self.count = [0,0]
        for x in xrange(settings.STAGE_WIDTH):
            for y in xrange(settings.STAGE_HEIGHT):
                self.count[self._map[x][y].owner]+=1
                self._map[x][y].update()
        Effect.effects.update()
        
    def draw(self):
        update_rect = []
#        for x in xrange(settings.STAGE_WIDTH):
#            for y in xrange(settings.STAGE_HEIGHT):
#                self._map[x][y].draw()
        update_rect += self.chips.draw(Game.get_screen())
        update_rect += self.unitmng.draw()
        update_rect += self.players.draw(Game.get_screen())
        #map(lambda u:u.draw(),self.players)
        update_rect += Effect.effects.draw(Game.get_screen())
        return update_rect
        
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
    
    def can_rotation(self, panels, player):
        owner = panels[0].owner
        if not owner is player: return False
        for panel in panels:
            if not panel.can_rotate(): return False
            if panel.owner != owner: return False
        return True
    
    def redraw_frame(self):
        u"""フレームを再描画する必要があるかどうか評価
        端っこの座標で回転するPanelSetがあるかどうか
        """
        for ps in self.panelsets:
            panel = ps.panels[0]
            if panel.point.x == 0 or panel.point.x == settings.STAGE_WIDTH-2 or panel.point.y == 0 or panel.point.y == settings.STAGE_HEIGHT-2: return True
        return False