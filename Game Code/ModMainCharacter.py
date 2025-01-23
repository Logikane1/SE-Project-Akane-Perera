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
    (0, 0, 90, 69),
    (90, 0, 90, 69),
    (180, 0, 90, 69),
    (270, 0, 90, 69),
    (360, 0, 90, 69),
    (450, 0, 90, 69)
]

deathSprites = [
    (0, 0, 48, 48),
    (48, 0, 48, 48),
    (96, 0, 48, 48),
    (144, 0, 48, 48),
    (192, 0, 48, 48),
    (240, 0, 48, 48),
    (288, 0, 48, 48),
    (336, 0, 48, 48),
    (384, 0, 48, 48)
]


class mainCharacter(pygame.sprite.Sprite):
    def __init__(self, position, face_right):
        super().__init__()
        
        idle_SpriteSheet = Spritesheet("Main_Assets/Spritesheets/Character/Idle/Idle.png", idleSprites)
        run_SpriteSheet = Spritesheet("Main_Assets/Spritesheets/Character/Running/Run.png", runSprites)
        attack_SpriteSheet = Spritesheet("Main_Assets/Spritesheets/Character/Attack/Attack.png", attackSprites)
        death_SpriteSheet = Spritesheet("Main_Assets/Spritesheets/Character/Death/Death.png", deathSprites)
        
        self.spriteSheets = {
            "IDLE" : idle_SpriteSheet,
            "RUN" : run_SpriteSheet,
            "ATTACK" : attack_SpriteSheet
            }
        
        self.animationIndex = 0
        self.facing_right = face_right
        self.currentState = "IDLE"
        self.x_direction = 0
        self.x_velocity = MC_SPEED 
        self.x_pos = position[0]
        self.y_pos = position[1]
        
        
    def update(self, level):
        
        self.previousState = self.currentState
        self.x_direction = 0
        
        if self.currentState != "ATTACK":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.currentState = "ATTACK"
            elif keys[pygame.K_a]:
                self.x_direction = -1
                self.facing_right = False
                self.currentState = "RUN"
            elif keys[pygame.K_d]:
                self.x_direction = 1
                self.facing_right = True
                self.currentState = "RUN"
            else:
                self.currentState = "IDLE"
        
        self.selectAnimation()
        
        if self.previousState != self.currentState: # reset animationIndex if the animation is changed 
            self.animationIndex = 0
            
        
        self.image = self.currentAnimation[int(self.animationIndex)]
        
        if self.currentState == "IDLE":
            self.rect = pygame.Rect(self.x_pos - 24, self.y_pos - 48, 48, 48) # since the x_pos and y_pos are at the bottom centre of the rect and we need to get the top left coordiante, we need to minus haf of the x and all of the y to get the top left 
        elif self.currentState == "RUN":
            self.rect = pygame.Rect(self.x_pos - 26.5, self.y_pos - 53, 53, 53)
        elif self.currentState == "ATTACK":
            self.rect = pygame.Rect(self.x_pos - 45, self.y_pos - 69, 90, 69)

        
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            self.animationIndex = 0
            self.currentState = "IDLE"
            
        self.x_move(level)
        
        self.checkEnemyCollisions(level.flying_eyes)
        
        
    
    def selectAnimation(self):
        self.animationSpeed = ANIMATIONSPEED_MC_DEFAULT
        if self.currentState == "IDLE":
            self.animationSpeed == ANIMATIONSPEED_MC_IDLE
            
        spriteSheet = self.spriteSheets[self.currentState]
        self.currentAnimation = spriteSheet.getSprites(flipped = not self.facing_right)


    def x_move(self, level):
        self.rect.centerx += self.x_direction * self.x_velocity
        
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        
        self.x_pos = self.rect.centerx
        
    def die(self):
        if self.currentState != "DIE":
            self.currentState = "DIE"
            self.animationIndex = 0

    def checkEnemyCollisions(self, enemies):
        collidedSprites = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in collidedSprites:
            if self.currentState == "ATTACK":
                if self.facing_right == True:
                    if enemy.rect.left < self.rect.right - 30:
                        enemy.die()
                else:
                    if enemy.rect.right > self.rect.left + 30:
                        enemy.die()
            else:
                if enemy.currentState != "DYING":
                    if self.rect.left < enemy.rect.left:
                        if self.rect.right > enemy.rect.left + 16:
                            self.die()
                    elif self.rect.right > enemy.rect.right:
                        if self.rect.left < enemy.rect.right - 16:
                            self.die()
                            