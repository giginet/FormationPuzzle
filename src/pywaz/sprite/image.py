# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
import pygame
from ..core.game import Game
from ..utils.vector import Vector
from math import cos, sin, radians
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
        self.change_image(filepath)
        self.area = area
        self.hit = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        self.x = x
        self.y = y
        self.center = Vector(self.rect.width/2, self.rect.height/2)

    @property
    def hit_area(self):
        x = self.rect.x + self.hit.x
        y = self.rect.y + self.hit.y
        w = self.hit.w
        h = self.hit.h
        return pygame.Rect(x, y, w, h)

    def change_image(self, filepath):
        self.image = pygame.image.load(filepath).convert_alpha()
        self.rect = self.image.get_rect()

    def _rotate(self, dest, center=None):
        if not center: center = self.center
        if not self.angle == 0 or not self.scale == 1:
            image = pygame.transform.rotozoom(self.image, self.angle, self.scale)
            srcc = Vector(self.image.get_size())*0.5
            radius = (srcc-center).length
            from math import atan2 
            theta = atan2(srcc.y-center.y,center.x-srcc.x) + radians(self.angle)
            dest = (Vector(self.x, self.y)-(Vector(image.get_size())*0.5 + Vector(cos(theta),-sin(theta))*radius))
            dest.x += center.x
            dest.y += center.y
            dest = dest.to_pos()
        else:
            image = self.image
        return image, dest

    def draw(self, surface=Game.get_screen(), dest=None, area=None, special_flags = 0):
        u"""Draw this sprite to the surface

        Argument:
            surface     - destination surface
            dest        - the `Rect` instance for using determine where to draw on the surface
            area        - the `Rect` instance for using determine where from draw on the sprite image
        """
        self.rect.x = self.x
        self.rect.y = self.y
        image = self.image
        if not dest: dest = self.rect
        if not area: area = self.area
        if not self.alpha == 255: image.set_alpha(self.alpha)
        image, dest = self._rotate(dest)
        return surface.blit(image, dest, area=area)