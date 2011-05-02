# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#
import settings

from pygame.rect import Rect
from pywaz.utils.singleton import Singleton
from pywaz.sprite import OrderedUpdates
from pywaz.core.game import Game
from pywaz.mixer.sound import Sound
from main.effect import Effect, AnimationInfo

from main.panel import DummyPanel
from main.utils import LocalPoint
from main.unit.attack import Attack
from main.unit.bomb import Bomb
from main.unit.guard import Guard
from main.unit.sweep import Sweep


class UnitManager(Singleton):
    def __init__(self, stage):
        self.stage = stage
        self.reset()
    def reset(self):
        self.units = []
    def remove(self, unit):
        if not unit: return
        unit.disappear()
        del self.units[self.units.index(unit)]
    def move_unit(self, unit, vector):
        u"""unitをvectorの方向に移動させる"""
        updates = []
        outdates = []
        for panel in unit.panels:
            next = self.stage.get_panel(panel.point+vector)
            if not next.unit: outdates.append(next)
        for panel in unit.panels:
            updates.append((panel, panel.point+vector))
            self.stage._map[panel.point.x][panel.point.y] = DummyPanel(panel.point.x, panel.point.y)
        for tuple in updates:
            panel = tuple[0]
            to = tuple[1]
            self.stage._map[to.x][to.y] = panel
            panel.point = to
        for panel in outdates:
            reverse = vector.clone().reverse()
            current_point = panel.point+reverse
            current_panel = self.stage.get_panel(current_point)
            while current_panel.unit:
                current_point = current_point + reverse
                current_panel = self.stage.get_panel(current_point)
            self.stage._map[current_point.x][current_point.y] = panel
            panel.point = current_point
            panel.change_owner(unit.owner)
        unit.move(outdates)
        map(lambda p: self.check(p), outdates)
    def battle(self, a, b):
        u"""ユニットaがユニットbを攻撃する"""
        b.hp -= a.attack
        if b.hp <= 0:
            self.remove(b)
        #ToDo エフェクト
        Sound(u'../resources/sound/battle_%s.wav' % a.name).play()
        v = a.degree
        for panel in a.panels:
            next = self.stage.get_panel(panel.point+v)
            if not a.owner == next.owner and next.unit:
                if v.x == 0:
                    y = [-32, -12]
                    Effect(u'../resources/effect/spark_horizonal.png', AnimationInfo(0,0,10,64,64,1), x=next.x+settings.PANELSIZE/2-32, y=panel.y+y[(v.y+1)/2])
                else:
                    x = [-32, -12]
                    Effect(u'../resources/effect/spark_vertical.png', AnimationInfo(0,0,10,64,64,1), x=panel.x+x[(v.x+1)/2], y=panel.y-(64-settings.PANELSIZE)/2)
        
    def draw(self):
        rects = []
        for unit in self.units:
            unit.draw()
            rects.append(unit.image.rect)
        return rects
    def get_unit_by_panel(self, panel):
        for unit in self.units:
            if unit.has(panel): return unit
    def check(self, panel):
        lp = panel.point
        unit = []
        for x in xrange(lp.x-2,lp.x+2):
            for y in xrange(lp.y-2,lp.y+2):
                unit.append(Sweep.generate(self.stage.get_panel(LocalPoint(x,y)), self.stage))
                unit.append(Attack.generate(self.stage.get_panel(LocalPoint(x,y)), self.stage))
        for x in xrange(lp.x-2,lp.x+2):
            for y in xrange(lp.y-2,lp.y+2):
                unit.append(Guard.generate(self.stage.get_panel(LocalPoint(x,y)), self.stage))
                if self.stage.bomb: unit.append(Bomb.generate(self.stage.get_panel(LocalPoint(x,y)), self.stage))
        u2 = []
        for u in unit:
            if u: 
                u2.append(u)
                
        if u2: self.units.extend(u2)