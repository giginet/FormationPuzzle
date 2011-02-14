# -*- coding: utf-8 -*-
#
#    Created on 2011/02/12
#    Created by giginet
#
import pygame

class Sound(object):
    def __init__(self, filepath):
        u"""ファイルから音声を読み込む"""
        class NoneSound:
            def play(self): pass
    
        if not pygame.mixer:
            return NoneSound()
    
        try:
            self.sound = pygame.mixer.Sound(filepath)
        except pygame.error:
            print u'''WARNING '%s' is not exist.''' % filepath
            raise IOError
        
    def play(self):
        self.sound.play()
