# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import pygame

from pywaz.scene.abstractscene import Scene
from pywaz.core.game import Game
from pywaz.sprite.image import Image
from pywaz.sprite.animation import Animation, AnimationInfo
from pywaz.mixer.bgm import BGM
from pywaz.utils.vector import Vector
from pywaz.utils.timer import Timer
from pywaz.device.mouse import Mouse

class LogoScene(Scene):
    BACKGROUND = (255,255,255)
    def ready(self):
        self.logo = Image("../resources/image/menu/logo.jpg", x=300, y=250)
        self.sprites.add(self.logo)
        self.timer = Timer(180)
        self.timer.play()
        
    def update(self):
        self.timer.tick()
        if self.timer.is_over() or Mouse.is_press('LEFT'):
            Game.get_scene_manager().change_scene('title')
        elif self.timer.now < 60:
            self.logo.alpha = 255*self.timer.now/60
        elif 120 < self.timer.now:
            self.logo.alpha = 255*(180-self.timer.now)/60
        
class TitleScene(Scene):
    def ready(self):
        self.bgm = BGM(u'../resources/bgm/title_intro.wav', -1, u'../resources/bgm/title_loop.wav')
        self.sprites.add(Image(u'../resources/image/menu/background.png'))
        self.bgm.play()
        
    def update(self):
        pass
        