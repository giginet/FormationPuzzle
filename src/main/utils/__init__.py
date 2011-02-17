import settings

from pywaz.utils.vector import Vector

class LocalPoint(Vector):
    def to_global(self):
        gx = settings.STAGE_OFFSET[0]+self.x*settings.PANELSIZE
        gy = settings.STAGE_OFFSET[1]+self.y*settings.PANELSIZE
        return Vector(gx,gy)
    def __add__(self, p):
        x = self.x + p.x
        y = self.y + p.y
        return LocalPoint(x,y)


def local_to_global(tuple):
    lx, ly = tuple
    return LocalPoint(lx,ly).to_global()
        
def global_to_local(tuple):
    gx, gy = tuple
    lx = int((gx - settings.STAGE_OFFSET[0])/settings.PANELSIZE)
    ly = int((gy - settings.STAGE_OFFSET[1])/settings.PANELSIZE)
    return LocalPoint(lx, ly)