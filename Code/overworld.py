from gameSettings import *
from sprites import Sprite, AnimatedSprite
from groups import WorldSprites

class Overworld:
    def __init__(self, tmx_map, data, overworld_frames):
        self.displaySurface = pygame.display.get_surface()
        self.data = data
        
        #groups
        self.allSprites = WorldSprites(data)
        
        self.setup(tmx_map, overworld_frames)
        
    def setup(self, tmx_map, overworld_frames):
        # tiles
        for layer in ['main', 'top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.allSprites, Z_LAYERS['bg tiles'])
                
        #water
        for column in range(tmx_map.width):
            for row in range(tmx_map.height):
                AnimatedSprite((column * TILE_SIZE, row * TILE_SIZE), overworld_frames['water'], self.allSprites, Z_LAYERS['bg'])

        #objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'palm':
                AnimatedSprite((obj.x, obj.y), overworld_frames['palms'], self.allSprites, Z_LAYERS['main'])
            else:
                z = Z_LAYERS[f'{'bg details' if obj.name == 'grass' else 'bg tiles'}']
                Sprite((obj.x, obj.y), obj.image, self.allSprites, )
        
    def run(self, dt):
        self.allSprites.update(dt)
        self.allSprites.draw((1000,800))