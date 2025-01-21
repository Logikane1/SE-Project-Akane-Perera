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
    
    
    
def load_block(size):
    path = join("assets", "Terrain", "terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32) # creates image of the designated size
    rect  = pygame.Rect(96, 0, size, size) # makes rectangle of at the position of thr top left hand side of the image
    surface.blit(image, (0, 0), rect ) # blits the image onto the surface
    return pygame.transform.scale2x(surface) # returns the image scaled by 2
    
    
        
        
        
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_spritesheets("Character", 32, 32, True)
    ANIMATION_DELAY = 2
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height) # uses rectangles to move the player
        self.x_velocity = 0
        self.y_velocity = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.gravity_count = 0
        self.jump_count = 0
        
    def jump(self):
        self.y_velocity = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
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
        self.y_velocity += min(1, (self.gravity_count / fps) * self.GRAVITY) # Calculates the amount of time the player has been falling and multiplies this by the gravity constant, this tells us how much to increment y.velocity
        self.move(self.x_velocity, self.y_velocity) #updates both velocity
        self.gravity_count += 1
        self.update_sprite()
            
    def update_sprite(self):
        spritesheet = "idle"
        if self.y_velocity < 0:
            if self.jump_count == 1:
                spritesheet = "jump"
            elif self.jump_count == 2:
                spritesheet = "double_jump"
        elif self.y_velocity > self.GRAVITY * 2:
            spritesheet = "fall"
        elif self.x_velocity != 0:
            spritesheet = "run"
        
        spritesheet_name = spritesheet + "_" + self.direction
        sprites = self.SPRITES[spritesheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites) # takes animation count, divides it by the animation delay value and mods whatever the line of the sprites
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
    
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) # constantly adjusts the width and height of the sprite image's rectangle using its x and y positions
        self.mask = pygame.mask.from_surface(self.sprite) # maps the pixels in the sprite (allows to perform pixel perfect collision)
    
    
    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
        

    def landed(self):
        self.gravity_count = 0 # stops adding gravity to player
        self.y_velocity = 0
        self.jump_count = 0 # for double jumping (added later)
        
    def hit_head(self):
        self.count = 0 
        self.y_velocity *= -1 # hits the player downwards


class Object(pygame.sprite.Sprite): # base class that defines all properties needed for sprites
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))
        
class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = load_block(size) # will make load_block later
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        
    


def create_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(WIDTH // width + 1): # tells how many tiles are needed to fill the width of the screen + 1 to make sure there are no gaps
        for j in range(HEIGHT // height + 1): # same as above but for y values
            position =(i * width, j * height)
            tiles.append(position)
    return tiles, image

def draw(game_window, background, bg_image, player, objects, offset_x): # draws the background
    for tile in background:
        game_window.blit(bg_image, tile)
        
    for o in objects:
        o.draw(game_window, offset_x)
    
    player.draw(game_window, offset_x)
    pygame.display.update()
        


def vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj): # passes the player and object and will tell us if they are colliding using the masks and rectangles of both of these
            if dy > 0:
                player.rect.bottom = obj.rect.top # places the character on top of the character it collided with to make sure it doesn't collide again
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom # same thing as above but if the player is in the air, it wil place the player below the object its colliding with
                player.hit_head()
        
        collided_objects.append(obj)
    
    return collided_objects





def handle_move(player, objects):
    keypress = pygame.key.get_pressed()
    
    player.x_velocity = 0
    
    if keypress[pygame.K_a]:
        player.move_left(PLAYER_VELOCITY)
    if keypress[pygame.K_d]:
        player.move_right(PLAYER_VELOCITY)
        
    vertical_collision(player, objects, player.y_velocity)





def main(game_window):
    
    clock = pygame.time.Clock()
    background, bg_image = create_background("Green.png")
    
    block_size = 96
    
    player = Player(100,100, 50, 50)
    blocks = [Block(0, HEIGHT - block_size, block_size)] # creates the block
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) 
            for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)] # creates blocks that generate in both x directions (basically creates floor for scrolling background)
    
    offset_x = 0 
    scroll_area_width = 200
    
    run = True
    while run:
        clock.tick(FPS) # sets the default Frame rate to 60
        
        for event in pygame.event.get(): # if player presses red x on their screen, application will close
            if event.type == pygame.QUIT:
                run = False
                break
            
            
            if event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
        
        player.loop(FPS)
        handle_move(player, floor)
        draw(game_window, background, bg_image, player, floor, offset_x)
    
    
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_velocity > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_velocity < 0):
            offset_x += player.x_velocity
    
    
    pygame.quit()
    quit()

if __name__ == "__main__":  # only calls main function if file is run directly 
    main(game_window)