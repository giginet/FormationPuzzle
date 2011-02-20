# -*- coding: utf-8 -*-
#
#    Created on 2011/02/21
#    Created by giginet
#
from pywaz.utils.singleton import Singleton
from main.panel import DummyPanel

class UnitManager(Singleton):
    units = []
    def __init__(self, stage):
        self.stage = stage
    def remove(self, unit):
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
        map(lambda p: self.stage.check(p), outdates)
    def battle(self, a, b):
        u"""ユニットaがユニットbを攻撃する"""
        b.hp -= a.attack
        print u"""%dのダメージ""" % a.attack
        if b.hp <= 0:
            print u"""敵ユニットをやっつけた！"""
            self.remove(b)
        #ToDo エフェクト
    def get_unit_by_panel(self, panel):
        for unit in self.units:
            if unit.has(panel): return unit
