from pywaz.sprite.animation import Animation, AnimationInfo
from main.utils import LocalPoint
from pywaz.utils.timer import Timer

from parameter import ATTACK

class Unit(object):
    animation_enable = False
    offset = (0,0)
    parameter = ATTACK
    degree = LocalPoint(0,0)
    
    def __init__(self, panels):
        self.panels = panels
        self.owner = panels[0].owner
        self.color = panels[0].color
        self.degree = LocalPoint(0, -1+self.owner*2)
        self.image = Animation(self.parameter['image'], AnimationInfo(self.owner,0,0,self.parameter['width'],self.parameter['height'],0))
        self.hp = self.parameter['hp']
        self.attack = self.parameter['attack']
        self.limit = self.parameter['limit']
        self.count = 0
        self.timer = Timer(self.parameter['frequency'])
        self.timer.play()
    
    @classmethod
    def generate(cls, panels, map):
        raise NotImplementedError
    
    @staticmethod
    def check(panels):
        color = panels[0].color
        owner = panels[0].owner
        for panel in panels:
            if not panel.can_unit() or not color == panel.color or not owner == panel.owner:
                return False
        else:
            return True
        
    def act(self):
        self.timer.tick()
        if self.timer.is_over():
            if self.count < self.limit:
                self.timer.reset()
                self.count+=1
                return 1
            else: return -1
        return
    
    def render(self):
        self.image.x, self.image.y = (self.panels[0].point + LocalPoint(self.offset)).to_global().to_pos()
        self.image.render()
        
    def get_front(self, vector):
        x, y = vector.to_pos()
        if x is 0 and y is -1:
            return self.panels.sort(cmp=lambda x, y: cmp(x.y,y.y))[0]
        elif x is 1 and y is 0:
            return self.panels.sort(cmp=lambda x, y: cmp(x.x,y.x), reverse=True)[0]
        elif x is 0 and y is 1:
            return self.panels.sort(cmp=lambda x, y: cmp(x.y,y.y), reverse=True)[0]
        elif x is -1 and y is 0:
            return self.panels.sort(cmp=lambda x, y: cmp(x.x,y.x))[0] 
        
    def has(self, panel): return panel in self.panels
    
    def disappear(self):
        for panel in self.panels: 
            panel.change_color()
            panel.unit = False