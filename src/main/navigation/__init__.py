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
        self.background = Image(u'../resources/image/main/navigation/background.png',x=self.X, y=self.Y)
        self.background.draw() 
        self.contents = OrderedUpdates()
        self.timer = NavigationTimer(75, x=74+self.X, y=178+self.Y)
        self.timer.play()
        self.stage = stage
        self.gauge = Gauge(x=self.X+10, y=self.Y+5)
    
    def update(self):
        self.timer.update()
        self.gauge.update(self.stage.calc_gauge())
    
    def draw(self):
        rects = self.timer.draw()
        rects += self.gauge.draw()
        return rects