import pygame
from Configuration import *
from ModSpriteSheet import Spritesheet


Flying_EyeSprites = [
    (0, 8, 47, 47),
    (64, 8, 47, 47),
    (128, 8, 47, 47),
    (192, 8, 47, 47),
    (256, 8, 47, 47),
    (320, 8, 47, 47),
    (384, 8, 47, 47),
    (448, 8, 47, 47),
]



class Flying_Eye():
    def __init__(self, position, move_right):
        
        
        self.eyeSpritesheet = Spritesheet(SPRITESHEET_PATH + "/Enemies/Flying Eye/Fly/Flight.png", Flying_EyeSprites)
        
        self.image = self.eyeSpritesheet.getSprites(move_right)[0]
        self.rect = self.image.get_rect(bottomleft = position)
        self.move_right = move_right

        self.animationCount = 0
        self.enemyState = "FLY"
    
    def update(self, level):
        if self.move_right == False:
            self.rect.x -= SPEED_FLYINGEYE
        else:
            self.rect.x += SPEED_FLYINGEYE
            
            
        if self.rect.right < 0:   # Makes the Flying Eye turn back when it exits the Window Screen
            self.move_right = True
        if self.rect.left > WINDOW_WIDTH:
            self.move_right = False
                
        self.selectAnimation()
        
        
        self.animationCount += self.animationSpeed
        if self.animationCount >= len(self.currentAnimation):
            self.animationCount = 0
            
        self.image = self.currentAnimation[int(self.animationCount)]
        
        self.image = self.eyeSpritesheet.getSprites(self.move_right)[0]
            
            
    def draw(self, displayWindow):
        displayWindow.blit(self.image, self.rect)
        
    def selectAnimation(self):
        self.animationSpeed = ANIMATIONSPEED_EYE
        if self.enemyState == "FLY":
            self.currentAnimation = self.eyeSpritesheet.getSprites(flipped = self.move_right)