# module for level class
import pygame
from Configuration import *
from Flying_Eye import *
from ModBackground import Background

class Level():
    def __init__(self, displayWindow):
        
        self.background = Background()
        self.flying_eye1 = Flying_Eye((200, 200))
        self.displayWindow = displayWindow
        
    def update(self):
        self.flying_eye1.update(self)
    
    def draw(self):
        self.background.draw(self.displayWindow)
        self.flying_eye1.draw(self.displayWindow)
    
    def run(self):
        self.update()
        self.run()