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
from pywaz.sprite.button import Button

class LogoScene(Scene):
    BACKGROUND = (255,255,255)
    def ready(self, *args, **kwargs):
        super(LogoScene, self).ready()
        self.logo = Image("../resources/image/menu/kawaz.png", x=273, y=244, alpha=False)
        self.sprites.add(self.logo)
        self.timer = Timer(210)
        
    def update(self):
        self.timer.tick()
        self.timer.play()
        if self.timer.is_over() or Mouse.is_press('LEFT'):
            Game.get_scene_manager().change_scene('title')
        elif self.timer.now < 60:
            self.logo.alpha = 255*self.timer.now/60
        elif 120 < self.timer.now:
            self.logo.alpha = 255*(180-self.timer.now)/60

class BombToggle(Button):
    def __init__(self, filepath, w, h, x=0, y=0):
        super(BombToggle, self).__init__(filepath,w,h,x,y)
        self.bomb = False
        
    def update(self):
        super(BombToggle, self).update()
        if self.bomb: self.ainfo.index = 1

    def on_release(self):
        self.bomb = not self.bomb

class TitleScene(Scene):
    def ready(self, *args, **kwargs):
        self.bgm = BGM(u'../resources/bgm/title_intro.wav', -1, u'../resources/bgm/title_loop.wav')
        self.logo = Image(u'../resources/image/menu/title/logo.png', x=80, y=-70)
        self.play = Button(u'../resources/image/menu/title/cpu.png', w=270, h=80, x=110, y=370)
        self.vs = Button(u'../resources/image/menu/title/2p.png', w=270, h=80, x=420, y=370)
        self.hard = BombToggle(u'../resources/image/menu/title/hard.png', w=270, h=80, x=110, y=470)
        self.exit = Button(u'../resources/image/menu/title/exit.png', w=270, h=80, x=420, y=470)
        self.exit.on_release = lambda: Game.get_scene_manager().exit()
        self.vs.on_release = lambda: Game.get_scene_manager().change_scene('game', self.hard.bomb, False)
        self.play.on_release = lambda: Game.get_scene_manager().change_scene('game', self.hard.bomb, True)
        for button in [self.play, self.vs, self.hard, self.exit]:
            button.hover_sound = '../resources/sound/on_cursor.wav'
            button.press_sound = '../resources/sound/selected.wav'
        self.sprites.add(Image(u'../resources/image/menu/background.png'),
                         self.logo,self.play,self.vs,self.hard,self.exit
        )
        self.timer = Timer(60)
        self.timer.play()
        
    def update(self):
        self.bgm.play()
        self.timer.tick()
        if self.timer.now < 15:
            self.logo.y = self.timer.now*10-70
        else: 
            self.logo.y = 80
            self.sprites.update()
        