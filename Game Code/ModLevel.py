# module for level class
import pygame
from Configuration import *
from ModMainCharacter import mainCharacter
from Flying_Eye import *
from ModBackground import Background

class Level():
    def __init__(self, displayWindow):
        
        self.background = Background()
        
        self.mainCharacter = mainCharacter((400, 400), face_right = True)
        self.flying_eye1 = Flying_Eye((200, 200), move_right = True)
        self.flying_eye2 = Flying_Eye((300, 300), move_right = False)
        
        self.displayWindow = displayWindow
        
    def update(self):
        self.mainCharacter.update(self)
        self.flying_eye1.update(self)
        self.flying_eye2.update(self)
    
    
    def draw(self):
        self.background.draw(self.displayWindow)
        self.mainCharacter.draw(self.displayWindow)
        self.flying_eye1.draw(self.displayWindow)
        self.flying_eye2.draw(self.displayWindow)
    
    def run(self):
        self.update()
        self.run()