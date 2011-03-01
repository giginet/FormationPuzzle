# -*- coding: utf-8 -*-
#
#    Created on 2011/03/01
#    Created by giginet
#
import pygame
from pywaz.core.game import Game
from pywaz.utils.singleton import Singleton
from pywaz.sprite.button import Button
from pywaz.sprite.image import Image
from pywaz.sprite import OrderedUpdates
from main.navigation.number import Number

class Result(Singleton):
    def __init__(self, stage, navigation):
        self.navigation = navigation
        self.stage = stage
        
    def ready(self):
        self.background = Image(u'../resources/image/main/result/background.png')
        self.gauge1 = Image(u'../resources/image/main/result/gauge1_full.png', x=60, y=160)
        self.gauge2 = Image(u'../resources/image/main/result/gauge2_full.png', x=60, y=160)
        self.retry = Button(u'../resources/image/main/result/retry.png', w=180, h=80, x=140, y=460)
        self.menu = Button(u'../resources/image/main/result/menu.png', w=180, h=80, x=480, y=460)
        self.minute = Number(0, u'../resources/image/main/result/time.png', x=420, y=306, w=60, h=75)
        self.second10 = Number(0, u'../resources/image/main/result/time.png', x=540, y=306, w=60, h=75)
        self.second1 = Number(0, u'../resources/image/main/result/time.png', x=600, y=306, w=60, h=75)
        self.sprites = OrderedUpdates(self.gauge2, self.gauge1, self.minute, self.second10, self.second1, self.retry, self.menu)
        self.retry.on_release = lambda : Game.get_scene_manager().change_scene('game',self.stage.bomb, self.stage.cpu)
        self.menu.on_release = lambda : Game.get_scene_manager().change_scene('title')
        for button in [self.retry, self.menu]:
            button.hover_sound = '../resources/sound/on_cursor.wav'
            button.press_sound = '../resources/sound/selected.wav'
        
        self.gauge1.xscale = float(self.navigation.gauge.proportion[0])/100
        
        m, s = self.navigation.timer.convert_time()
        self.minute.n = m
        if s < 10:
            self.second10.n = 0
            self.second1.n = s
        else:
            self.second10.n = int(str(s)[0])
            self.second1.n = int(str(s)[1])    
        
        if self.stage.count[0] > self.stage.count[1]:
            self.sprites.add(Image(u'../resources/image/main/result/win.png', x=80, y=160))
            self.sprites.add(Image(u'../resources/image/main/result/lose.png', x=480, y=160))
        elif self.stage.count[0] < self.stage.count[1]:
            self.sprites.add(Image(u'../resources/image/main/result/win.png', x=480, y=160))
            self.sprites.add(Image(u'../resources/image/main/result/lose.png', x=80, y=160))
        else:
            self.sprites.add(Image(u'../resources/image/main/result/draw.png', x=280, y=170))
        
        
    def draw(self, surface=Game.get_screen()):
        self.background.draw()
        self.navigation.background.draw(self.navigation.image)
        self.sprites.draw(Game.get_screen())
    def update(self):
        self.sprites.update()