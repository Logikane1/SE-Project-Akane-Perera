# module for level class
import pygame
from Configuration import *

class Level():
    def __init__(self, displayWindow):
        
        self.displayWindow = displayWindow
        self.backgroundImage = pygame.image.load(SPRITESHEET_PATH + "/Archon_Sky.png").convert()
        self.backgroundImage = pygame.transform.scale(self.backgroundImage, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
    def update(self):
        pass
    
    def draw(self):
        self.displayWindow.blit(self.backgroundImage,(0, 0))
    
    def run(self):
        self.update()
        self.run()