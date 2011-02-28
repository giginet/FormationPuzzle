import pygame
import settings

from pywaz.utils.singleton import Singleton
from pywaz.sprite.image import Image
from pywaz.sprite import OrderedUpdates
from pywaz.core.game import Game

from main.navigation.timer import Timer as NavigationTimer
from main.navigation.gauge import Gauge

class Navigation(Singleton):
    X = 675
    Y = 20
    
    def __init__(self, stage):
        self.image = pygame.surface.Surface((98,558))
        self.image.set_colorkey((0,0,0))
        self.background = Image(u'../resources/image/main/navigation/background.png')
        self.background.draw(self.image)
        self.contents = OrderedUpdates()
        self.timer = NavigationTimer(settings.TIME, x=46, y=82)
        self.timer.play()
        self.stage = stage
        self.gauge = Gauge(x=10, y=5)
        self.update()
    
    def update(self):
        self.timer.update()
        self.gauge.update(self.stage.calc_gauge())
    
    def draw(self):
        rects = self.timer.draw(self.image)
        rects += self.gauge.draw(self.image)
        Game.get_screen().blit(self.image, self.image.get_rect().move(self.X, self.Y))
        return []