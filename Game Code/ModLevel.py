# module for level class
import pygame
from Configuration import *
from ModMainCharacter import mainCharacter
from Flying_Eye import *
from ModBackground import Background

class Level():
    def __init__(self, displayWindow):
        
        self.background = Background()
        
        self.MainCharacter = pygame.sprite.GroupSingle()
        self.flying_eyes = pygame.sprite.Group()
        
        self.MainCharacter.add(mainCharacter((400, 400), face_right = True))
        self.flying_eyes.add(Flying_Eye((200, 200), move_right = True))
        self.flying_eyes.add(Flying_Eye((300, 380), move_right = False))
        
        self.displayWindow = displayWindow
        
    def update(self):
        self.MainCharacter.update(self)
        self.flying_eyes.update(self)
    
    
    def draw(self):
        self.background.draw(self.displayWindow)
        self.MainCharacter.draw(self.displayWindow)
        self.flying_eyes.draw(self.displayWindow)
    
    def run(self):
        self.update()
        self.run()