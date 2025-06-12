from gameSettings import *
from sprites import Sprite, AnimatedSprite, Node, Icon, PathSprite
from groups import WorldSprites
from random import randint

class Overworld:
    def __init__(self, tmx_map, data, overworld_frames, switch_stage):
        self.displaySurface = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage
        
        #Initialise Groups
        self.allSprites = WorldSprites(data)
        self.nodeSprites = pygame.sprite.Group()
        
        # Setup overworld tiles, nodes, objects, paths, and icon
        self.setup(tmx_map, overworld_frames)
        
        # Identify the current node based on player progress
        self.currentNode = [node for node in self.nodeSprites if node.level == 0][0]
        
        # Store path frame images and create visual path tiles
        self.path_frames = overworld_frames['path']
        self.create_path_sprites()
        
    def setup(self, tmx_map, overworld_frames):
        # static tile background for the overworld
        for layer in ['main', 'top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.allSprites, Z_LAYERS['bg tiles'])
                
        # animated water tiles across the map
        for column in range(tmx_map.width):
            for row in range(tmx_map.height):
                AnimatedSprite((column * TILE_SIZE, row * TILE_SIZE), overworld_frames['water'], self.allSprites, Z_LAYERS['bg'])

        #Create environment objects like palms or grass
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'palm':
                # Randomize palm animation speed for visual variety
                AnimatedSprite((obj.x, obj.y), overworld_frames['palms'], self.allSprites, Z_LAYERS['main'], randint(4, 6))
            else:
                # Choose Z layer based on object type (e.g. grass is on 'bg details')
                z_key = 'bg details' if obj.name == 'grass' else 'bg tiles'
                z = Z_LAYERS[z_key]
                Sprite((obj.x, obj.y), obj.image, self.allSprites, )
                
        # paths connecting nodes from Tiled map properties 
        self.paths = {}
        for obj in tmx_map.get_layer_by_name('Paths'): # Convert path points into pixel positions
            pos = [(int(p.x + TILE_SIZE / 2), int(p.y + TILE_SIZE / 2)) for p in obj.points]
            start = obj.properties['start']
            end = obj.properties['end']
            self.paths[end] = {'pos': pos, 'start': start}
            
                
        #Setup all nodes and place the player's icon at the current level
        for obj in tmx_map.get_layer_by_name('Nodes'):
            
            #player
            if obj.name == 'Node' and obj.properties['stage'] == self.data.current_level:
                self.icon = Icon((obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), self.allSprites, overworld_frames['icon'])
            
            # Collect path directions (left/right/up/down) from Tiled properties
            if obj.name == 'Node':
                available_paths = {k:v for k, v in obj.properties.items() if k in ('left', 'right', 'up', 'down')}
                Node(
                    pos = (obj.x, obj.y), 
                    surf = overworld_frames['path']['node'], 
                    groups = (self.allSprites, self.nodeSprites),
                    level = obj.properties['stage'],
                    data = self.data,
                    paths = available_paths)
        
    def create_path_sprites(self): # translates logical paths between nodes into visual tile sprites. It determines direction and corner types to match path tiles.
        # get tiles for path
        nodes = {node.level : vector(node.grid_pos) for node in self.nodeSprites}
        path_tiles = {}
        
        for path_id, data in self.paths.items():
            path = data['pos']
            start_node, end_node = nodes[data['start']], nodes[path_id]
            path_tiles[path_id] = [start_node]
            
            # Convert vector path into tile positions
            for index, points in enumerate(path): # going through all of the points in path
                if index < len(path) - 1: # to prevent index error
                    start, end = vector(points), vector(path[index + 1]) # get the start point and end point of the current path and store it as a vector
                    path_dir = (end - start) /TILE_SIZE
                    start_tile = vector(int(start[0] / TILE_SIZE), int(start[1]/ TILE_SIZE))
                    
                    if path_dir.y:
                        dir_y = 1 if path_dir.y > 0 else - 1
                        for y in range(dir_y, int(path_dir.y) + dir_y, dir_y):
                            path_tiles[path_id].append(start_tile + vector(0,y))
                    
                    if path_dir.x:
                        dir_x = 1 if path_dir.x > 0 else - 1
                        for x in range(dir_x, int(path_dir.x) + dir_x, dir_x):
                            path_tiles[path_id].append(start_tile + vector(x,0))
            
            path_tiles[path_id].append(end_node)
            
        # create sprites
        for key, path in path_tiles.items():
            for index, tile in enumerate(path):
                if index > 0 and index < len(path) - 1:
                    previous_tile = path[index - 1] - tile
                    next_tile = path[index + 1] - tile
                    
                    if previous_tile.x == next_tile.x:
                        surf = self.path_frames['vertical']
                    elif previous_tile.y == next_tile.y:
                        surf = self.path_frames['horizontal']
                    else:
                        if previous_tile.x == -1 and next_tile.y == -1 or previous_tile.y == -1 and next_tile.x == -1:
                            surf = self.path_frames['tl']
                        elif previous_tile.x == 1 and next_tile.y == 1 or previous_tile.y == 1 and next_tile.x == 1:
                            surf = self.path_frames['br']
                        elif previous_tile.x == -1 and next_tile.y == 1 or previous_tile.y == 1 and next_tile.x == -1:
                            surf = self.path_frames['bl']
                        elif previous_tile.x == 1 and next_tile.y == -1 or previous_tile.y == -1 and next_tile.x == 1:
                            surf = self.path_frames['tr']
                        else:
                            surf = self.path_frames['horizontal'] # safety net incase something in path goes wrong
                            
                        
                    PathSprite(
                        pos = (tile.x * TILE_SIZE, tile.y * TILE_SIZE), 
                        surf = surf, 
                        groups = self.allSprites, 
                        level = key)
            
    def input(self): # basic oveworld movement
        keys = pygame.key.get_pressed()
        if self.currentNode and not self.icon.path:
            if keys[pygame.K_s] and self.currentNode.can_move('down'):
                self.move('down')
            if keys[pygame.K_a] and self.currentNode.can_move('left'):
                self.move('left')
            if keys[pygame.K_d] and self.currentNode.can_move('right'):
                self.move('right')
            if keys[pygame.K_w] and self.currentNode.can_move('up'):
                self.move('up')
            if keys[pygame.K_RETURN]:
                # Set the new current level and switch to the level scene
                self.data.current_level = self.currentNode.level
                self.switch_stage('level')
                
    def move(self, direction): # Called when the player chooses to move in a valid direction
        path_key = int(self.currentNode.paths[direction][0])
        path_reverse = True if self.currentNode.paths[direction][-1] == 'r' else False # if node path has a r in it, reverse
        path = self.paths[path_key]['pos'][:] if not path_reverse else self.paths[path_key]['pos'][::-1] # gives the points of the position of the node, if reverse reverse the list with ::-1
        self.icon.start_move(path)
        
    def get_current_node(self): # Checks if the icon overlaps with a node and updates the currentNode
        nodes = pygame.sprite.spritecollide(self.icon, self.nodeSprites, False)
        if nodes:
            self.currentNode = nodes[0]
        
    def run(self, dt):
        self.input()
        self.get_current_node()
        self.allSprites.update(dt)
        self.allSprites.draw(self.icon.rect.center)
        