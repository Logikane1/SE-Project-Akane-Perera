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

Flying_Eye_HitSprites = [
    (0, 0, 52, 52),
    (52, 0, 52, 52),
    (104, 0, 52, 52),
    (156, 0, 52, 52)
]

class Flying_Eye(pygame.sprite.Sprite):
    def __init__(self, position, move_right):
        super().__init__()
        
        self.eyeSpritesheet = Spritesheet(SPRITESHEET_PATH + "/Enemies/Flying Eye/Fly/Flight.png", Flying_EyeSprites)
        self.eye_attackSpriteSheet = Spritesheet(SPRITESHEET_PATH + "/Enemies/Flying Eye/Attack/Enemy Attack 1.png", Flying_Eye_AttackSprites)
        self.eye_hitSpritesheet = Spritesheet(SPRITESHEET_PATH + "/Enemies/Flying Eye/Hit/Hit.png", Flying_Eye_HitSprites)
        
        self.image = self.eyeSpritesheet.getSprites(move_right)[0]
        self.rect = self.image.get_rect(bottomleft = position)
        self.y_direction = 0
        self.moving_right = move_right
        self.animationCount = 0
        self.currentState = "FLY"
    
    def update(self, level):
        if self.moving_right == False:
            self.rect.x -= SPEED_FLYINGEYE
        else:
            self.rect.x += SPEED_FLYINGEYE
            
            
        if self.rect.right < 0:   # Makes the Flying Eye turn back when it exits the Window Screen
            self.moving_right = True
        if self.rect.left > WINDOW_WIDTH:
            self.moving_right = False
            
            
        if self.currentState == "DYING":
            self.y_direction += GRAVITY
            self.rect.y += self.y_direction
            if self.rect.top > WINDOW_HEIGHT:
                self.kill()
            
        mainCharacterRect = level.MainCharacter.sprite.rect
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
            if self.currentState == "ATTACK" or self.currentState == "DYING":
                self.animationCount = len(self.currentAnimation) - 1
            else:
                self.currentState == "FLY"
                self.animationCount = 0
            
        self.image = self.currentAnimation[int(self.animationCount)]
            
        
    def selectAnimation(self):
        self.animationSpeed = ANIMATIONSPEED_EYE
        if self.currentState == "FLY":
            self.currentAnimation = self.eyeSpritesheet.getSprites(flipped = self.moving_right)
        elif self.currentState == "ATTACK":
            self.animationSpeed == ANIMATIONSPEED_ATTACK_EYE
            self.currentAnimation = self.eye_attackSpriteSheet.getSprites(flipped = self.moving_right)
        else:
            self.currentAnimation = self.eye_hitSpritesheet.getSprites(flipped = self.moving_right)
            
    def die(self):
        if self.currentState != "DYING":
            self.animationCount = 0
            self.currentState = "DYING"