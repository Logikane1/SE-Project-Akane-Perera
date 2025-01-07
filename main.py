import os 
import math
import random
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("The Archon") # Window Application Name

WIDTH, HEIGHT = 1000, 700
FPS = 60
PLAYER_VELOCITY = 5

game_window = pygame.display.set_mode((WIDTH, HEIGHT)) # Creates Window for Game to Appear

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites] # True and False determines if we flip in the x direction or not

def load_spritesheets(dir1, width, height, direction=False):
    path = join("assets", dir1 )
    images = [f for f in listdir(path) if isfile(join(path, f))] # will load every file in the directory
    
    allsprites = {}
    
    for image in images:
        spritesheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        for i in range(spritesheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(spritesheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            allsprites[image.replace(".png", "") + "_right"] = sprites
            allsprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            allsprites[image.replace(".png", "")] + sprites
    
    return allsprites
    
    
    
# def get_block(size):
#    path = join("assets", "Terrain")
        
        
        
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_spritesheets("Character", 32, 32, True)
    ANIMATION_DELAY = 3
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height) # uses rectangles to move the player
        self.x_velocity = 0
        self.y_velocity = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.gravity_count = 0
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
    def move_left(self, velocity):
        self.x_velocity = -velocity # use negative velocity to move left 
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
            
    def move_right(self, velocity):
        self.x_velocity = velocity # use negative velocity to move left 
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
        
    def loop(self, fps):
        # self.y_velocity += min(1, (self.gravity_count / fps) * self.GRAVITY) # Calculates the amount of time the player has been falling and multiplies this by the gravity constant, this tells us how much to increment y.velocity
        self.move(self.x_velocity, self.y_velocity) #updates both velocity
        self.gravity_count += 1
        self.update_sprite()
        
        
    def update_sprite(self):
        spritesheet = "idle"
        if self.x_velocity != 0:
            spritesheet = "run"
        
        spritesheet_name = spritesheet + "_" + self.direction
        sprites = self.SPRITES[spritesheet_name]
        sprite_index = (self.animation_count //  self.ANIMATION_DELAY) % len(sprites) # takes animation count, divides it by the animation delay value and mods whatever the line of the sprites
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
    
    
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) # constantly adjusts the width and height of the sprite image's rectangle using its x and y positions
        self.mask = pygame.mask.from_surface(self.sprite) # maps the pixels in the sprite (allows to perform pixel perfect collision)
    
    
    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))
        





class Object(pygame.sprite.Sprite): # base class that defines all properties needed for sprites
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
        
#class Block(Object):
#    def __init__(self, x, y, size):
#        super().__init__(x, y, size, size)
#        block = load_block(size) # will make load_block later
#        self.image.blit(block, (0, 0))
#        self.mask = pygame.mask.from_surface(self.image)
        
    







def create_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(WIDTH // width + 1): # tells how many tiles are needed to fill the width of the screen + 1 to make sure there are no gaps
        for j in range(HEIGHT // height + 1): # same as above but for y values
            position =(i * width, j * height)
            tiles.append(position)
    return tiles, image

def draw(game_window, background, bg_image, player): # draws the background
    for tile in background:
        game_window.blit(bg_image, tile)
        
    player.draw(game_window)
    pygame.display.update()
        
def handle_move(player):
    keypress = pygame.key.get_pressed()
    player.x_velocity = 0
    
    if keypress[pygame.K_a]:
        player.move_left(PLAYER_VELOCITY)
    if keypress[pygame.K_d]:
        player.move_right(PLAYER_VELOCITY)





def main(game_window):
    
    clock = pygame.time.Clock()
    background, bg_image = create_background("Green.png")
    
    player = Player(100,100, 50, 50)
    
    run = True
    while run:
        clock.tick(FPS) # sets the default Frame rate to 60
        
        for event in pygame.event.get(): # if player presses red x on their screen, application will close
            if event.type == pygame.QUIT:
                run = False
                break
        player.loop(FPS)
        handle_move(player)
        draw(game_window, background, bg_image, player)
    pygame.quit()
    quit()

if __name__ == "__main__":  # only calls main function if file is run directly 
    main(game_window)