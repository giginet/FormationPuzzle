# -*- coding: utf-8 -*-
#
#    Created on 2011/03/01
#    Created by giginet
#
import pygame
from pywaz.core.game import Game
from pywaz.utils.singleton import Singleton
from pywaz.sprite.button import Button
from pywaz.sprite import OrderedUpdates

class Result(Singleton):
    def __init__(self):
        self.image = pygame.surface.Surface()
        self.menu = Button(u'../resources/image/main/result/menu.png')
        self.sprites = OrderedUpdates(self.menu)
    
    def draw(self, surface=Game.get_screen()):
        self.sprites.draw(Game.get_screen())
    
    def update(self):
        self.sprites.update()