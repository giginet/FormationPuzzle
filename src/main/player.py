# -*- coding: utf-8 -*-
#
#    Created on 2011/02/17
#    Created by giginet
#
import pygame
from pygame.locals import *
import settings

from pywaz.sprite.animation import Image
from pywaz.device.mouse import Mouse
from pywaz.device.key import Key
from pywaz.device.joypad import JoyPad
from pywaz.utils.timer import Timer

from main.utils import global_to_local, LocalPoint, local_to_global

class Player(Image):
    pressed = False
    initial_position = (
                        (settings.STAGE_WIDTH-1, settings.STAGE_HEIGHT-1),
                        (0,0),
    )
    
    def __init__(self, n, interfaces=None):
        self.number = n
        self.x, self.y = local_to_global(self.initial_position[n]).to_pos()
        self.point = LocalPoint(self.initial_position[n])
        self.interfaces = [] 
        super(Player, self).__init__(u'../resources/image/main/player/cursor.png', area=pygame.rect.Rect(0,n*40,40,40),x=100, y=100)
        self.animation_enable = False
        self.joy = JoyPad()
        if not interfaces: self.set_type()
        else: self.interfaces = interfaces
        self.press_counter = [0,0,0,0,0,0]
        self.key_mode = False
        self.pre_mouse_point = LocalPoint(0,0)
        
    def set_type(self):
        count = self.joy.get_count()
        print self.number, self.interfaces   
        if count == 0:
            types = ('mouse','key')
        elif count == 1:
            types = ('mouse', 'pad')
        else:
            types = ('pad', 'pad')
        self.interfaces.append(types[self.number])

    def update(self):
        u'''
        なにかキーが押されたらkey_mode=True。このとき、マウス操作は利かない
        マウス座標が前と変わったら、key_mode=False
        '''
        if not self.pre_mouse_point == self.get_mouse_point(): self.key_mode = False
        if 'mouse' in self.interfaces and not self.key_mode: 
            self.point = self.get_mouse_point()
            if self.in_map():
                Mouse.hide_cursor()
            else: 
                Mouse.show_cursor()
        if 'key' in self.interfaces:
            if Key.is_press(K_UP):
                self.press_counter[0] += 1
                self.key_mode = True
            elif Key.is_press(K_DOWN):
                self.press_counter[1] += 1
                self.key_mode = True
            if Key.is_press(K_LEFT):
                self.press_counter[2] += 1
                self.key_mode = True
            elif Key.is_press(K_RIGHT):
                self.press_counter[3] += 1
                self.key_mode = True
        if 'pad' in self.interfaces:
            if self.joy.get_count() == 1: id = 0
            else: id = self.number
            if self.joy.sticks[id].get_button(14):
                self.press_counter[0] += 1
            elif self.joy.sticks[id].get_button(11):
                self.press_counter[1] += 1
            if self.joy.sticks[id].get_button(13):
                self.press_counter[2] += 1
            elif JoyPad.sticks[id].get_button(12):
                self.press_counter[3] += 1
        if self.press_counter[0] > 1:
            self.press_counter[0] = 0
            self.point.y -= 1
        if self.press_counter[1] > 1:
            self.press_counter[1] = 0
            self.point.y += 1
        if self.press_counter[2] > 1:
            self.press_counter[2] = 0
            self.point.x -= 1
        if self.press_counter[3] > 1:
            self.press_counter[3] = 0
            self.point.x += 1
        if self.point.x < 0: self.point.x = 0
        elif self.point.x > settings.STAGE_WIDTH-2: self.point.x = settings.STAGE_WIDTH-2
        if self.point.y < 0: self.point.y =0
        elif self.point.y > settings.STAGE_HEIGHT-2: self.point.y = settings.STAGE_HEIGHT-2
        self.move_pointer()
        self.pre_mouse_point = self.get_mouse_point()
        
    def move_pointer(self):
        if self.in_map():
            self.x, self.y = self.point.to_global().add(LocalPoint(1,1)).to_pos()
            self.rect.x = self.x
            self.rect.y = self.y    
        
    def poll(self):
        if 'mouse' in self.interfaces and not self.key_mode:
            if Mouse.is_press('LEFT') and not self.pressed:
                self.pressed = True
                return 1
            elif Mouse.is_press('RIGHT') and not self.pressed:
                self.pressed = True
                return -1
            if Mouse.is_release(self):
                self.pressed = False
        if 'key' in self.interfaces:
            if Key.is_press(K_x): 
                if not self.press_counter[4]:
                    self.press_counter[4] = 1
                    self.key_mode = True
                    return -1
            elif Key.is_press(K_z):
                if not self.press_counter[5]: 
                    self.press_counter[5] = 1
                    self.key_mode = True
                    return 1
            else:
                self.press_counter[4] = 0
                self.press_counter[5] = 0
        return 0
    
    def get_mouse_point(self):
        return global_to_local(Mouse.get_pos())
    
    def in_map(self):
        lp = self.point
        return 0 <= lp.x < settings.STAGE_WIDTH-1 and 0 <= lp.y < settings.STAGE_HEIGHT-1
    
import random
class NPC(Player):
    def __init__(self, n):
        super(NPC, self).__init__(n)
        self.act_timer = Timer(1)
        self.goal = LocalPoint(0,0)
        self.interfaces = ['npc']
        self.rotate = False
        
    def update(self):
        self.act_timer.tick()
        if self.point == self.goal:
            self.goal = LocalPoint(random.randint(0,settings.STAGE_WIDTH),random.randint((1-self.number)*settings.STAGE_WIDTH/2,(1-self.number)*settings.STAGE_WIDTH/2+settings.STAGE_WIDTH/2-3))
            self.rotate = True
        else:
            if not self.act_timer.is_over(): return
            sub = self.goal - self.point
            if sub.x >0:
                self.point.x +=1
            elif sub.x < 0:
                self.point.x -=1
            if sub.y >0:
                self.point.y +=1
            elif sub.y < 0:
                self.point.y -=1
        self.move_pointer()
        self.act_timer.reset()
        self.act_timer.play()
        
    def poll(self):
        if self.rotate:
            self.rotate = False
            return random.choice([-1,1])