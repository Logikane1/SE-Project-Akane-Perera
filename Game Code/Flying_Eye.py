import pygame
from Configuration import *
from ModSpriteSheet import Spritesheet


Flying_EyeSprites = [
    (16, 0, 47, 47),
    (80, 0, 47, 47),
    (144, 0, 47, 47),
    (208, 0, 47, 47),
    (272, 0, 47, 47),
    (336, 0, 47, 47),
    (400, 0, 47, 47),
    (464, 0, 47, 47),
]



class Flying_Eye():
    def __init__(self, position, move_right):
        
        
        self.eyeSpritesheet = Spritesheet(SPRITESHEET_PATH + "/Enemies/Flying Eye/Fly/Flight.png", Flying_EyeSprites)
        
        self.image = self.eyeSpritesheet.getSprites(move_right)[0]
        self.rect = self.image.get_rect(bottomleft = position)
        self.move_right = move_right
    
    def update(self, level):
        if self.move_right == False:
            self.rect.x -= SPEED_FLYINGEYE
        else:
            self.rect.x += SPEED_FLYINGEYE
            
            
        if self.rect.right < 0:   # Makes the Flying Eye turn back when it exits the Window Screen
            self.move_right = True
        if self.rect.left > WINDOW_WIDTH:
            self.move_right = False
            
        self.image = self.eyeSpritesheet.getSprites(self.move_right)[0]
            
            
    
            
    def draw(self, displayWindow):
        displayWindow.blit(self.image, self.rect)