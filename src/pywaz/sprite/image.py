# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame
from ..core.game import Game
from ..utils.vector import Vector
from math import cos, sin, atan2, hypot, radians

class Image(pygame.sprite.Sprite):
    angle = 0
    scale = 1
    alpha = 255
    
    def __init__(self, filepath, area=None, x=0, y=0):
        u"""Constructor of Sprite class

        Argument:
            image       - image surface of this Sprite
            area        - represents a smaller portion of the source to draw
        """
        super(Image, self).__init__()
        self.image = pygame.image.load(filepath).convert()
        self.rect = self.image.get_rect()
        self.area = area
        self.hit = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        self.x = x
        self.y = y
        self.center = Vector(self.rect.width/2, self.rect.height/2) #回転時の中心座標相対位置

    @property
    def hit_area(self):
        x = self.rect.x + self.hit.x
        y = self.rect.y + self.hit.y
        w = self.hit.w
        h = self.hit.h
        return pygame.Rect(x, y, w, h)

    def render(self, surface=Game.get_screen(), dest=None, area=None, special_flags = 0):
        u"""Draw this sprite to the surface

        Argument:
            surface     - destination surface
            dest        - the `Rect` instance for using determine where to draw on the surface
            area        - the `Rect` instance for using determine where from draw on the sprite image
        """
        self.rect.x = self.x
        self.rect.y = self.y
        image = self.image
        if not dest:
            dest = self.rect
        if not area:
            area = self.area
        if not self.angle == 0 or self.scale == 1:
            image = pygame.transform.rotozoom(self.image, self.angle, self.scale)
            #元画像と変換後の画像の差分を取る（じゃないとゲッダンするので）
            # 元画像の中心位置  
            srcc = Vector(self.image.get_size())*0.5
            # 中心座標から見た座標Aの角度と距離を基準にする  
            radius = (srcc-self.center).length  
            theta = (srcc-self.center).angle + radians(self.angle)
            # base_posの移動量    
            # 回転画像の左上を基準にしたbase_posのドットの位置  
            dest = (Vector(self.x, self.y)-(Vector(image.get_size())*0.5 + Vector(radius * cos(theta), -radius * sin(theta)))).to_pos()
        if not self.alpha == 255:
            image.set_alpha(self.alpha)
        return surface.blit(image, dest, area=area)