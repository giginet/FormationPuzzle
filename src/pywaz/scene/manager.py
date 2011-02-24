# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
class SceneManager(object):
    def __init__(self):
        self._scenes_dict = {}
        self._current_scene = None
        
    def set_scene(self, dict):
        self._scenes_dict.update(dict)
    
    def set_scenes(self, dict):
        self._scenes_dict = dict
        
    def change_scene(self, key):
        if self._scenes_dict.has_key(key):
            if self.current_scene:  self.current_scene.finalize()
            self._current_scene = self._scenes_dict[key]
            self.current_scene.ready()
        
    @property
    def current_scene(self):
        if self.is_empty():
            return None
        return self._current_scene
    
    def is_empty(self):
        return not self._current_scene
        
    def update(self):
        if not self.is_empty():
            self.current_scene.update()
    
    def draw(self):
        if not self.is_empty():
            return self.current_scene.draw()