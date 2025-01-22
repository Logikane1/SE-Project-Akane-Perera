# module for level class
import pygame
from Configuration import *
from ModBackground import Background

class Level():
    def __init__(self, displayWindow):
        
        self.background = Background()
        self.displayWindow = displayWindow
        
    def update(self):
        pass
    
    def draw(self):
        self.background.draw(self.displayWindow)
    
    def run(self):
        self.update()
        self.run()