import pygame
from Configuration import *

class Flying_Eye():
    def __init__(self, position):
        
        flying_eyeImage = pygame.image.load(SPRITESHEET_PATH + "/Enemies/Flying Eye/Fly/Flight.png")
        self.image = flying_eyeImage.subsurface(pygame.Rect(16, 0, 47, 47))
        self.rect = self.iamge.get_rect(bottomleft = position)
    
    def update(self, level):
        pass
    
    def draw(self, displayWindow):
        displayWindow.blit(self.image, self.rect)