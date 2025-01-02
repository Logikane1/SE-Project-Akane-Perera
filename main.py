import os 
import math
import random
import pygame
from os import listdr
from os.path import isfile, join

pygame .init()

pygame.display.set_caption("The Archon") # Window Application Name

WIDTH, HEIGHT = 10000, 700
FPS = 60
PLAYER_VELOCITY = 5

game_window = pygame.display.set_mode((WIDTH, HEIGHT)) # Creates Window for Game to Appear

class Player(pygame.sprite.Sprite):
    COLOUR = (255, 0, 0)
    GRAVITY = 1
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height) # uses rectangles to move the player
        self.x_velocity = 0
        self.y_velocity = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.gravity_count = 0
        
        
def create_background(name):
    image = pygame.image.load(join("assests", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(WIDTH // width + 1): # tells how many tiles are needed to fill the width of the screen + 1 to make sure there are no gaps
        position =(i * width, j * height) # same as above but for y values
        tiles.append(position)
    return tiles, image

def main(game_window):
    clock = pygame.time.Clock()
    background, bg_image = create_background()
    
    player = Player(100,100, 50, 50)
    
    run = True
    while run:
        clock.tick(FPS) # sets the default Frame rate to 60
        
        for event in pygame.event.get(): # if player presses red x on their screen, application will close
            if event.type == pygame.QUIT:
                run = False
                break
        player.loop(FPS)
    pygame.quit()
    quit()

if __name__ == "__main__":  # only calls main function if file is run directly 
    main(game_window)