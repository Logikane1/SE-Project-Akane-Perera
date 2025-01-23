import pygame 
from Configuration import *
from ModSpriteSheet import Spritesheet

idleSprites = [
    (16, 0, 48, 48),
    (80, 0, 48, 48),
    (144, 0, 48, 48),
    (208, 0, 48, 48),
    (272, 0, 48, 48),
    (336, 0, 48, 48),
    (400, 0, 48, 48),
    (464, 0, 48, 48),
    (528, 0, 48, 48),
    (592, 0, 48, 48),
    (656, 0, 48, 48)
]

runSprites = [
    (11, 0, 53, 53),
    (75, 0, 53, 53),
    (139, 0, 53, 53),
    (203, 0, 53, 53),
    (267, 0, 53, 53),
    (331, 0, 53, 53),
    (395, 0, 53, 53),
    (459, 0, 53, 53)
]

attackSprites = [
    (0, 0, 91, 91),
    (91, 0, 91, 91),
    (182, 0, 91, 91),
    (263, 0, 91, 91),
    (344, 0, 91, 91),
    (425, 0, 91, 91)
]



class mainCharacter():
    def __init__(self, position, face_right):
        
        idle_SpriteSheet = Spritesheet("Main_Assets/Spritesheets/Character/Idle/Idle.png", idleSprites)
        run_SpriteSheet = Spritesheet("Main_Assets/Spritesheets/Character/Running/Run.png", runSprites)
        attack_SpriteSheet = Spritesheet("Main_Assets/Spritesheets/Character/Attack/Attack.png", attackSprites)
        
        self.spriteSheets = {
            "IDLE" : idle_SpriteSheet,
            "RUN" : run_SpriteSheet,
            "ATTACK" : attack_SpriteSheet
            }
        
        self.animationIndex = 0
        self.facing_right = face_right
        self.currentState = "IDLE"
        self.x_pos = position[0]
        self.y_pos = position[1]
        
        
    def update(self, level):
        self.selectAnimation()
        self.image = self.currentAnimation[int(self.animationIndex)]
        if self.currentState == "IDLE":
            self.rect = pygame.Rect(self.x_pos - 24, self.y_pos - 48, 48, 48) # since the x_pos and y_pos are at the bottom centre of the rect and we need to get the top left coordiante, we need to minus haf of the x and all of the y to get the top left 
            
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            self.animationIndex = 0
            self.currentState = "IDLE"
            
    
    def draw(self, displayWindow):
        displayWindow.blit(self.image, self.rect)
    
    def selectAnimation(self):
        self.animationSpeed = ANIMATIONSPEED_MC_DEFAULT
        if self.currentState == "IDLE":
            self.animationSpeed == ANIMATIONSPEED_MC_IDLE
            
        spriteSheet = self.spriteSheets[self.currentState]
        self.currentAnimation = spriteSheet.getSprites(flipped = not self.facing_right)
        