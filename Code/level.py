from gameSettings import *
from sprites import Sprite
from player import Player

class Level:
    def __init__(self, tmx_map):
        self.displayWindow = pygame.display.get_surface()
        
        #groups
        self.allSprites = pygame.sprite.Group()
        self.collisionSprites = pygame.sprite.Group()
        
        self.setup(tmx_map)
        
    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.allSprites, self.collisionSprites))
            
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == "Player":
                Player((obj.x, obj.y), self.allSprites, self.collisionSprites)
                
                
    def run(self, dt):
        self.allSprites.update(dt)
        self.displayWindow.fill('black')
        self.allSprites.draw(self.displayWindow)