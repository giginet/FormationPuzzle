# -*- coding: utf-8 -*-
#
#    Created on 2011/03/01
#    Created by giginet
#
from pygame.rect import Rect

from pywaz.scene.abstractscene import Scene
from pywaz.utils.singleton import Singleton
from pywaz.sprite.image import Image
from pywaz.sprite.animation import AnimationInfo, Animation
from pywaz.utils.timer import Timer
from pywaz.device.mouse import Mouse

class ReadySequence(Scene, Singleton):
    def __init__(self, frame, background):
        super(ReadySequence, self).__init__()
        self.frame = frame
        self.background = background
        self.string = Animation(u'../resources/image/main/strings.png',AnimationInfo(-1,0,0,360,210,0),x=220, y=195)
        self.string.animation_enable = False
        self.timer = Timer(240)
    
    def ready(self):
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
    
    def ready(self):
        self.navigation.timer.play()
        
    def update(self):
        super(MainSequence, self).update()
        self.stage.update()
        self.navigation.update()
        called = (settings.STAGE_WIDTH*settings.STAGE_HEIGHT)*settings.CALLED
        if self.stage.count[0] > called or self.stage.count[1] > called: return 'result' 
        if self.navigation.timer.is_over(): return 'result'

from main.result import Result
from pywaz.mixer.bgm import BGM
class ResultSequence(Scene, Singleton):
    def __init__(self, navigation, frame):
        super(ResultSequence,self).__init__()
        self.navigation = navigation
        self.frame = frame
        self.window = Result(navigation)
        
    def ready(self):
        Mouse.show_cursor()
        self.bgm = BGM(u'../resources/bgm/result_intro.wav', -1, u'../resources/bgm/result_loop.wav')
        self.bgm.play()
        self.window.ready()
    
    def update(self):
        self.window.update()
    
    def draw(self):
        self.frame.draw()
        self.window.draw()
        return []

class PauseSequence(Scene, Singleton):
    pass