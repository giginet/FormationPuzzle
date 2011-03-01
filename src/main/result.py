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

class Result(Singleton):
    def __init__(self, navigation):
        self.navigation = navigation
        self.background = Image(u'../resources/image/main/result/background.png')
        self.player1 = Image(u'../resources/image/main/result/1p.png', x=63, y=40)
        self.player2 = Image(u'../resources/image/main/result/2p.png', x=583, y=40)
        self.gauge1 = Image(u'../resources/image/main/result/gauge1_full.png', x=63, y=180)
        self.gauge2 = Image(u'../resources/image/main/result/gauge2_full.png', x=63, y=180)
        self.retry = Button(u'../resources/image/main/result/retry.png', w=180, h=80, x=143, y=460)
        self.menu = Button(u'../resources/image/main/result/menu.png', w=180, h=80, x=443, y=460)
        self.sprites = OrderedUpdates(self.player1, self.player2, self.gauge2, self.gauge1, self.retry, self.menu)
        self.retry.on_release = lambda : Game.get_scene_manager().change_scene('game')
        self.menu.on_release = lambda : Game.get_scene_manager().change_scene('title')
        for button in [self.retry, self.menu]:
            button.hover_sound = '../resources/sound/on_cursor.wav'
            button.press_sound = '../resources/sound/selected.wav'
    def ready(self):
        self.gauge1.xscale = float(self.navigation.gauge.proportion[0])/100
        
    def draw(self, surface=Game.get_screen()):
        self.background.draw()
        self.navigation.background.draw(self.navigation.image)
        self.sprites.draw(Game.get_screen())
    def update(self):
        self.sprites.update()