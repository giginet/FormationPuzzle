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
from pywaz.device.key import Key

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
    while 1:
        game._clock.tick(60)
        #game._screen.fill(game.current_scene().BACKGROUND) # 画面のクリア
        Key.poll()
        game.act()
        game.render()
        #pygame.display.update([Rect(0,0,1,1)]) # 画面を反映
        for event in pygame.event.get(): # イベントチェック
            if event.type == QUIT: # 終了が押された？
                return
            if (event.type == KEYDOWN and
                event.key  == K_ESCAPE): # ESCが押された？
                return
if __name__ == '__main__': main()