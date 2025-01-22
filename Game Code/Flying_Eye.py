import pygame
from Configuration import *

class Flying_Eye():
    def __init__(self, position, move_right):
        
        flying_eyeImage = pygame.image.load(SPRITESHEET_PATH + "/Enemies/Flying Eye/Fly/Flight.png")
        self.image = flying_eyeImage.subsurface(pygame.Rect(16, 0, 47, 47))
        self.rect = self.image.get_rect(bottomleft = position)
        self.move_right = move_right
    
    def update(self, level):
        if self.move_right == False:
            self.rect.x -= SPEED_FLYINGEYE
        else:
            self.rect.x += SPEED_FLYINGEYE
            
    def draw(self, displayWindow):
        displayWindow.blit(self.image, self.rect)