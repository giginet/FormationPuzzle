from pywaz.utils.singleton import Singleton
from pywaz.sprite.image import Image
from pywaz.sprite import OrderedUpdates
from pywaz.core.game import Game

from main.navigation.timer import Timer as NavigationTimer


class Navigation(Singleton):
    X = 690
    Y = 30
    
    def __init__(self):
        self.background = Image(u'../resources/image/main/navigation/background.png',x=self.X, y=self.Y)
        self.timer = NavigationTimer(120, x=50+self.X, y=80+self.Y)
        self.timer.play()
    
    def update(self):
        self.timer.update()
    
    def draw(self):
        rects = self.timer.draw()
        return rects