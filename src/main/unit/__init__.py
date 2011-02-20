from pywaz.sprite.animation import Animation, AnimationInfo
from main.utils import LocalPoint

class Unit(object):
    filepath = u"../resources/image/main/unit/attack.png"
    animation_enable = False
    offset = (0,0)
    
    def __init__(self, panels):
        self.panels = panels
        self.owner = panels[0].owner
        self.color = panels[0].color
        self.image = Animation(self.filepath, AnimationInfo(self.owner,0,0,60,60,0))
    
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