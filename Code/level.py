from gameSettings import *
from sprites import Sprite, MovingSprite
from player import Player
from groups import AllSprites

class Level:
    def __init__(self, tmx_map):
        self.displayWindow = pygame.display.get_surface()
        
        #groups
        self.allSprites = AllSprites()
        self.collisionSprites = pygame.sprite.Group()
        self.semicollisionSprites = pygame.sprite.Group()
        
        self.setup(tmx_map)
        
    def setup(self, tmx_map):
        #tiles
        for layer in ['Background', 'Terrain', 'Platforms', 'Foreground']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.allSprites]
                if layer == 'Terrain': groups.append(self.collisionSprites)
                if layer == 'Platforms': groups.append(self.semicollisionSprites)
                z = Z_LAYERS['bg tiles']
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)
            
        #objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.allSprites, self.collisionSprites, self.semicollisionSprites)
                
        #moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'helicopter':
                if obj.width > obj.height: # horizontal movement
                    move_dir = 'x'
                    start_position = (obj.x, obj.y + obj.height / 2)
                    end_position = (obj.x + obj.width, obj.y + obj.height / 2)
                else:
                    move_dir = 'y'
                    start_position = (obj.x + obj.width / 2, obj.y)
                    end_position = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite((self.allSprites, self.semicollisionSprites), start_position, end_position, move_dir, speed)
                
                
                
    def run(self, dt):
        self.displayWindow.fill('black')
        self.allSprites.update(dt)
        self.allSprites.draw(self.player.hitboxRect.center)