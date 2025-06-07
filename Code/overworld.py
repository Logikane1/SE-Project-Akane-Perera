from gameSettings import *
from sprites import Sprite, AnimatedSprite, Node, Icon
from groups import WorldSprites
from random import randint

class Overworld:
    def __init__(self, tmx_map, data, overworld_frames):
        self.displaySurface = pygame.display.get_surface()
        self.data = data
        
        #groups
        self.allSprites = WorldSprites(data)
        self.nodeSprites = pygame.sprite.Group()
        
        self.setup(tmx_map, overworld_frames)
        
        self.currentNode = [node for node in self.nodeSprites if node.level == 0][0]
        
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
                AnimatedSprite((obj.x, obj.y), overworld_frames['palms'], self.allSprites, Z_LAYERS['main'], randint(4, 6))
            else:
                z = Z_LAYERS[f'{'bg details' if obj.name == 'grass' else 'bg tiles'}']
                Sprite((obj.x, obj.y), obj.image, self.allSprites, )
                
        # paths 
        self.paths = {}
        for obj in tmx_map.get_layer_by_name('Paths'):
            pos = [(int(p.x + TILE_SIZE / 2), int(p.y + TILE_SIZE / 2)) for p in obj.points]
            start = obj.properties['start']
            end = obj.properties['end']
            self.paths[end] = {'pos': pos, 'start': start}
        print(self.paths)
            
                
        # nodes and player
        for obj in tmx_map.get_layer_by_name('Nodes'):
            
            #player
            if obj.name == 'Node' and obj.properties['stage'] == self.data.current_level:
                self.icon = Icon((obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), self.allSprites, overworld_frames['icon'])
            
            #nodes
            if obj.name == 'Node':
                available_paths = {k:v for k, v in obj.properties.items() if k in ('left', 'right', 'up', 'down')}
                Node(
                    pos = (obj.x, obj.y), 
                    surf = overworld_frames['path']['node'], 
                    groups = (self.allSprites, self.nodeSprites),
                    level = obj.properties['stage'],
                    data = self.data,
                    paths = available_paths)
        
    def input(self):
        keys = pygame.key.get_pressed()
        if self.currentNode:
            if keys[pygame.K_s] and self.currentNode.can_move('down'):
                self.move('down')
            
    def move(self, direction):
        path_key = int(self.currentNode.paths[direction][0])
        path_reverse = True if self.currentNode.paths[direction][-1] == 'r' else False # if node path has a r in it, reverse
        path = self.paths[path_key]['pos'][:] if not path_reverse else self.paths[path_key]['pos'][::-1] # gives the points of the position of the node, if reverse reverse the list with ::-1
        self.icon.start_move(path)
        
    def run(self, dt):
        self.input()
        self.allSprites.update(dt)
        self.allSprites.draw(self.icon.rect.center)
        