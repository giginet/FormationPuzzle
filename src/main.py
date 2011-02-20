# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import pygame
from pygame.locals import *

import settings

from pywaz.core.game import Game
from pywaz.scene.abstractscene import Scene

from scene.menu import *
from scene.game import *

def main():
    pygame.mixer.pre_init(44100, -16, 2, 1024*3)
    pygame.init() # pygameの初期化
    game = Game()
    game.set_caption(u"Kawaz")
    game.get_scene_manager().set_scenes({'logo':LogoScene(),'game':GameScene(), 'title':TitleScene()})
    if settings.DEBUG:
        game.get_scene_manager().change_scene('game')
    else:
        game.get_scene_manager().change_scene('logo')
    return game.mainloop()

if __name__ == '__main__': main()