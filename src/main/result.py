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
    def __init__(self):
        self.image = pygame.surface.Surface((800,600))
        self.background = Image(u'../resources/image/main/result/background.png')
        self.player1 = Image(u'../resources/image/main/result/1p.png', x=63, y=40)
        self.player2 = Image(u'../resources/image/main/result/2p.png', x=583, y=40)
        self.retry = Button(u'../resources/image/main/result/retry.png', w=180, h=80, x=143, y=460)
        self.menu = Button(u'../resources/image/main/result/menu.png', w=180, h=80, x=443, y=460)
        self.sprites = OrderedUpdates(self.background, self.player1, self.player2, self.retry, self.menu)
        self.retry.on_release = lambda : Game.get_scene_manager().change_scene('game')
        self.menu.on_release = lambda : Game.get_scene_manager().change_scene('title')
    
    def draw(self, surface=Game.get_screen()):
        self.sprites.draw(Game.get_screen())
    
    def update(self):
        self.sprites.update()