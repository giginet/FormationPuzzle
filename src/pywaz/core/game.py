# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame
from pygame.locals import *

from ..utils.singleton import Singleton
from window import Window
from ..scene.manager import SceneManager
from ..device.key import Key

class Game(Singleton):
    _clock = pygame.time.Clock()
    _scene_manager = SceneManager()
    _screen = Window(width=800, height=600, caption=u"Hello,Kawaz!")
        
    @classmethod
    def get_screen(cls):
        return cls._screen.window
    
    @classmethod
    def act(cls):
        cls._scene_manager.act()
        
    @classmethod
    def render(cls):
        cls._scene_manager.render()
        
    @classmethod
    def get_scene_manager(cls):
        return cls._scene_manager
    
    @classmethod
    def current_scene(cls):
        return cls._scene_manager.current_scene
    
    @classmethod
    def set_caption(cls, caption):
        pygame.display.set_caption(caption)
    
    @classmethod
    def mainloop(cls):
        while 1:
            cls._clock.tick(60)
            cls._screen.fill(cls.current_scene().BACKGROUND) # 画面のクリア
            Key.poll()
            cls.act()
            cls.render()
            pygame.display.flip() # 画面を反映
            for event in pygame.event.get(): # イベントチェック
                if event.type == QUIT: # 終了が押された？
                    return
                if (event.type == KEYDOWN and
                    event.key  == K_ESCAPE): # ESCが押された？
                    return