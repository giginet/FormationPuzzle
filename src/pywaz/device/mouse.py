# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame
from pygame.locals import *
from ..utils.singleton import Singleton

class Mouse(Singleton):
    
    def __init__(self):
        raise NotImplementedError
    
    @staticmethod
    def is_press(key):
        MOUSENAME = {'LEFT':0,
                 'CENTER':1,
                 'RIGHT':2
        }
        return pygame.mouse.get_pressed()[MOUSENAME[key]]
    
    @staticmethod
    def get_pos():
        return pygame.mouse.get_pos()
    
    @staticmethod
    def show_cursor():
        pygame.mouse.set_visible(True)
        
    @staticmethod
    def hide_cursor():
        pygame.mouse.set_visible(False)