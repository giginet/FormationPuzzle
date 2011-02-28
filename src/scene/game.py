# -*- coding: utf-8 -*-
#
#    Created on 2011/02/14
#    Created by giginet
#
import settings
import pygame

from pywaz.sprite.image import Image
from pywaz.mixer.bgm import BGM
from pywaz.scene.manager import SceneManager
from pywaz.scene.abstractscene import Scene
from main.sequences import ReadySequence, MainSequence, ResultSequence, PauseSequence

from main.stage import Stage
from main.navigation import Navigation

class GameScene(Scene):
    def ready(self):
        self.background = settings.BACKGROUND
        self.frame = Image(u'../resources/image/main/frame.png', x=settings.STAGE_OFFSET[0]-15, y=settings.STAGE_OFFSET[1]-15)
        self.stage = Stage()
        self.bgm = BGM(u'../resources/bgm/game_intro.wav', -1, u'../resources/bgm/game_loop.wav')
        self.background.draw()
        self.frame.draw()
        self.navigation = Navigation(self.stage)
        self.sequence_mng = SceneManager({'ready':ReadySequence(self.frame, self.background),
                                          'main': MainSequence(self.stage, self.navigation), 
                                          'result':ResultSequence(self.navigation, self.frame), 
                                          'pause':PauseSequence()})
        self.sequence_mng.change_scene('ready')
        
    def update(self):
        super(GameScene, self).update()
        #if not settings.DEBUG: 
        self.bgm.play()
        next = self.sequence_mng.current_scene.update()
        if next: 
            #self.background.draw()
            self.sequence_mng.change_scene(next)
        
    def draw(self):
        super(GameScene, self).draw()
        if self.stage.redraw_frame(): self.frame.draw() #マップのはじで回転させたとき、回転の軌跡が残ってしまうため、フレームを再描画
        rect_draw = self.stage.draw()
        rect_draw += self.navigation.draw()
        rect_draw += self.sequence_mng.current_scene.draw()
        return rect_draw