import pygame
from Configuration import *

class Spritesheet():
    def __init__(self, spritesheet_path, sprite_positions):
        image = pygame.image.load(spritesheet_path).convert_alpha()
        self.sprites = []
        self.spritesFlipped = []
        
        for position in sprite_positions:
            sprite = image.subsurface(pygame.Rect(position))
            self.sprites.append(sprite)
            sprite = pygame.transform.flip(sprite, True, False) # flips horizontally only
            self.spritesFlipped.append(sprite)
            
    def getSprites(self, flipped):
        if flipped == True:
            return self.spritesFlipped
        else:
            return self.sprites