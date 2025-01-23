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
    (448, 8, 47, 47)
]


Flying_Eye_AttackSprites = [
    (0, 0, 52, 52),
    (52, 0, 52, 52),
    (104, 0, 52, 52),
    (156, 0, 52, 52),
    (208, 0, 52, 52),
    (260, 0, 52, 52),
    (312, 0, 52, 52),
    (364, 0, 52, 52)
]


class Flying_Eye():
    def __init__(self, position, move_right):
        
        
        self.eyeSpritesheet = Spritesheet(SPRITESHEET_PATH + "/Enemies/Flying Eye/Fly/Flight.png", Flying_EyeSprites)
        self.attackSpriteSheet = Spritesheet(SPRITESHEET_PATH + "/Enemies/Flying Eye/Attack/Enemy Attack 1.png", Flying_Eye_AttackSprites)
        
        self.image = self.eyeSpritesheet.getSprites(move_right)[0]
        self.rect = self.image.get_rect(bottomleft = position)
        self.move_right = move_right

        self.animationCount = 0
        self.currentState = "FLY"
    
    def update(self, level):
        if self.move_right == False:
            self.rect.x -= SPEED_FLYINGEYE
        else:
            self.rect.x += SPEED_FLYINGEYE
            
            
        if self.rect.right < 0:   # Makes the Flying Eye turn back when it exits the Window Screen
            self.move_right = True
        if self.rect.left > WINDOW_WIDTH:
            self.move_right = False
            
        mainCharacterRect = level.mc.rect
        mainCharacterX = mainCharacterRect.centerx
        
        if self.currentState == "FLY":
            if mainCharacterRect.top < self.rect.bottom <= mainCharacterRect.bottom:
                if self.moving_right == True:
                    if self.rect.left < mainCharacterX and self.rect.right > mainCharacterX - 50:
                        self.currentState = "ATTACK"
                        self.animationCount = 0
                else:
                    if self.rect.right > mainCharacterX and self.rect.left < mainCharacterX + 50:
                        self.currentState = "ATTACK"
                        self.animationCount = 0
        elif self.currentState == "ATTACK":
            if self.moving_right == True:
                if self.rect.left >= mainCharacterX or self.rect.right < mainCharacterX - 50:
                    self.currentState = "FLY"
                    self.animationCount = 0
            else:
                if self.rect.right <= mainCharacterX or self.rect.left > mainCharacterX + 50:
                    self.currentState = "FLY"
                    self.animationCount = 0
            
            
                
        self.selectAnimation() 
        
        
        self.animationCount += self.animationSpeed  # each times animation is updated, the count is increased by 1 to the next frame
        if self.animationCount >= len(self.currentAnimation): # after reaching the last frame, it goes back to the original first frame [0]
            if self.currentState == "ATTACK":
                self.animationCount = len(self.currentAnimation) - 1
            else:
                self.currentState == "FLY"
                self.animationCount = 0
            
        self.image = self.currentAnimation[int(self.animationCount)]
            
            
    def draw(self, displayWindow):
        displayWindow.blit(self.image, self.rect)
        
    def selectAnimation(self):
        self.animationSpeed = ANIMATIONSPEED_EYE
        if self.currentState == "FLY":
            self.currentAnimation = self.eyeSpritesheet.getSprites(flipped = self.move_right)