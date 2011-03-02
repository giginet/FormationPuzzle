# -*- coding: utf-8 -*-
#
#    Created on 2011/03/01
#    Created by giginet
#
from pygame.locals import *

from pygame.rect import Rect

from pywaz.scene.abstractscene import Scene
from pywaz.utils.singleton import Singleton
from pywaz.sprite.image import Image
from pywaz.sprite.animation import AnimationInfo, Animation
from pywaz.utils.timer import Timer
from pywaz.device.mouse import Mouse
from pywaz.device.key import Key
from pywaz.mixer.sound import Sound

class ReadySequence(Scene, Singleton):
    def __init__(self, frame, background):
        super(ReadySequence, self).__init__()
        self.frame = frame
        self.background = background
        self.string = Animation(u'../resources/image/main/strings.png',AnimationInfo(-1,0,0,360,210,0),x=220, y=195)
        self.string.animation_enable = False
        self.timer = Timer(240)
    
    def ready(self, *args, **kwargs):
        BGM.set_volume(0.4)
        self.timer.play()
    
    def update(self):
        self.timer.tick()
        if self.timer.now == 30:
            self.string.ainfo.index = 0
        elif self.timer.now == 60:
            BGM.set_volume(1)
            self.string.ainfo.index = 1
        elif 60 < self.timer.now < 70:
            self.string.y -= 30
        elif self.timer.now == 70:
            self.background.draw()
            self.frame.draw()
            return 'main'
        
    def draw(self):
        self.string.draw()
        return []

import settings
class MainSequence(Scene, Singleton):
    def __init__(self, stage, navigation):
        super(MainSequence, self).__init__()
        self.stage = stage
        self.navigation = navigation
    
    def ready(self, *args, **kwargs):
        self.navigation.timer.play()
        self.press_pause = True
        self.crisis = False
        
    def update(self):
        super(MainSequence, self).update()
        self.stage.update()
        self.navigation.update()
        u"""ポーズへの移行"""
        if not Key.is_press(K_RETURN):
            self.press_pause = False
        if not self.press_pause and Key.is_press(K_RETURN): 
            Sound(u'../resources/sound/pause.wav').play()
            return 'pause'
        u"""リミットの9割に達したとき、音を鳴らす"""
        crisis = (settings.STAGE_WIDTH*settings.STAGE_HEIGHT)*settings.CALLED*0.9
        if self.stage.count[0] > crisis or self.stage.count[1] > crisis: 
            if not self.crisis:
                self.crisis = True
                Sound(u'../resources/sound/area_crisis.wav').play()
        else: self.crisis = False
        u"""ゲーム終了判定"""
        called = (settings.STAGE_WIDTH*settings.STAGE_HEIGHT)*settings.CALLED
        if self.stage.count[0] > called or self.stage.count[1] > called: return 'result' 
        if self.navigation.timer.is_over(): return 'result'

from main.result import Result
from pywaz.mixer.bgm import BGM
class ResultSequence(Scene, Singleton):
    def __init__(self, stage, navigation, frame):
        super(ResultSequence,self).__init__()
        self.stage = stage
        self.navigation = navigation
        self.frame = frame
        self.window = Result(stage, navigation)
        
    def ready(self, *args, **kwargs):
        Mouse.show_cursor()
        self.bgm = BGM(u'../resources/bgm/result_intro.wav', -1, u'../resources/bgm/result_loop.wav')
        self.bgm.play()
        self.window.ready()
        self.draw()
    
    def update(self):
        self.window.update()
    
    def draw(self):
        self.frame.draw()
        self.window.draw()
        return [Rect(0,0, 800, 600)]

class PauseSequence(Scene, Singleton):
    def ready(self, *args, **kwargs):
        BGM.set_volume(0.4)
        self.press = True
        Mouse.show_cursor()
        self.string = Animation(u'../resources/image/main/strings.png',AnimationInfo(3,0,0,360,210,0),x=220, y=195)
    
    def draw(self):
        self.string.draw()
        return []
        
    def update(self):
        if not Key.is_press(K_RETURN):
            self.press = False
        if not self.press and Key.is_press(K_RETURN):
            Sound(u'../resources/sound/pause.wav').play()
            BGM.set_volume(1)
            return 'main'