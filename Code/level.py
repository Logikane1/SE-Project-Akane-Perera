from gameSettings import *
from sprites import Sprite, AnimatedSprite, MovingSprite, Spike, Item, ParticleEffectSprite
from player import Player
from groups import AllSprites
from random import uniform
from enemies import Tooth, Shell, Pearl
from gameTimer import Timer

class Level:
    def __init__(self, tmx_map, level_frames, audio_files, data, switch_stage):
        self.displayWindow = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage
        
        #level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE # basically level_height
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
        self.level_unlock = tmx_level_properties['level_unlock']
        if tmx_level_properties['bg']: # background tile is selected based on level properties; fallback is None if not specified
            bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
        else:
            bg_tile = None
            
        #groups
        # Create the main sprite group for managing all rendering and camera scrolling.
        # Also includes environmental features like clouds and background tiles.
        self.allSprites = AllSprites(
            width = tmx_map.width, 
            height = tmx_map.height,
            bg_tile = bg_tile,
            top_limit = tmx_level_properties['top_limit'],
            clouds = {'large': level_frames['cloud_large'], 'small': level_frames['cloud_small']},
            horizon_line = tmx_level_properties['horizon_line'])
        
        self.collisionSprites = pygame.sprite.Group()
        self.semicollisionSprites = pygame.sprite.Group()
        self.damageSprites = pygame.sprite.Group()
        self.toothSprites = pygame.sprite.Group()
        self.pearlSprites = pygame.sprite.Group()
        self.itemSprites = pygame.sprite.Group()
        
        self.setup(tmx_map, level_frames, audio_files)
        
        #frames
        self.pearl_surf = level_frames['pearl']
        self.particle_frames = level_frames['particle']
        
        #audio
        self.coin_sfx = audio_files['coin']
        self.coin_sfx.set_volume(0.4)
        
        self.damage_sfx = audio_files['damage']
        self.damage_sfx.set_volume(0.9)
        self.damage_sfx_timer = Timer(500)
        
        self.pearl_sfx = audio_files['pearl']
        
    def setup(self, tmx_map, level_frames, audio_files):
        #tiles
        # Loop through each visual/interactive layer and place tiles accordingly.
        # Some tiles are collision-only, others are decorative. 
        for layer in ['Background', 'Terrain', 'Platforms', 'Foreground']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.allSprites]
                # Add collision groups based on layer type
                if layer == 'Terrain': groups.append(self.collisionSprites)
                if layer == 'Platforms': groups.append(self.semicollisionSprites)
                # Assign correct z-layer for rendering order
                match layer:
                    case 'Background': z = Z_LAYERS['bg tiles']
                    case 'Foreground': z = Z_LAYERS['bg tiles']
                    case _: z = Z_LAYERS['main']
                    
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)
        #bg details
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == 'static':
                Sprite((obj.x, obj.y), obj.image, self.allSprites, z = Z_LAYERS['bg tiles'])
            else:
                AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.allSprites, z = Z_LAYERS['bg tiles'], animation_speed = ANIMATION_SPEED)
        #objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == "Player":
                self.player = Player(
                    pos = (obj.x, obj.y), 
                    groups = self.allSprites, 
                    collision_sprites = self.collisionSprites, 
                    semicollision_sprites = self.semicollisionSprites,
                    frames = level_frames['player'],
                    data = self.data,
                    attack_sfx = audio_files['attack'],
                    jump_sfx = audio_files['jump'])
                
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image, (self.allSprites, self.collisionSprites))
                else:
                    frames = level_frames[obj.name] if not 'dark_tree' in obj.name else level_frames['dark_trees'][obj.name]
                    if obj.name == 'floor_spikes' and obj.properties['inverted']:
                        frames = [pygame.transform.flip(frame, False, True) for frame in frames]
                        
                    groups = [self.allSprites]
                    if obj.name in('dark_tree'): groups.append(self.semicollisionSprites)
                    if obj.name in('fire_trap', 'floor_spikes'): groups.append(self.damageSprites)
                    
                    z = Z_LAYERS['main'] if not 'bg' in obj.name else Z_LAYERS['bg details']
                    
                    animation_speed = ANIMATION_SPEED if not 'dark_tree' in obj.name else ANIMATION_SPEED + uniform(-1, 1)
                        
                    AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)

            if obj.name == 'flag':
                self.level_finish_rect = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))
        #moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == "spike":
                # Set up moving spike enemies in a circular arc path
                # Uses the start and end angle from Tiled properties to determine movement arc
                Spike(
                    pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
                    surf = level_frames['spike'],
                    radius = obj.properties['radius'],
                    speed = obj.properties['speed'],
                    start_angle = obj.properties['start angle'],
                    end_angle = obj.properties['end angle'],
                    groups = (self.allSprites, self.damageSprites))
                for radius in range(0, obj.properties['radius'], 20):
                    # Create spike chains visually connecting to main spike enemy
                    Spike(
                        pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
                        surf = level_frames['spike_chain'],
                        radius = radius,
                        speed = obj.properties['speed'],
                        start_angle = obj.properties['start angle'],
                        end_angle = obj.properties['end angle'],
                        groups = self.allSprites,
                        z = Z_LAYERS['bg details'])
                
            else:
                frames = level_frames[obj.name]
                groups = (self.allSprites, self.semicollisionSprites) if obj.properties['platform'] else (self.allSprites, self.damageSprites)
                # Logic for horizontal or vertical moving platforms
                if obj.width > obj.height: # horizontal moving platforms
                    move_dir = 'x'
                    start_position = (obj.x, obj.y + obj.height / 2)
                    end_position = (obj.x + obj.width, obj.y + obj.height / 2)
                else: # vertical moving platforms
                    move_dir = 'y'
                    start_position = (obj.x + obj.width / 2, obj.y)
                    end_position = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite(frames, groups, start_position, end_position, move_dir, speed, obj.properties['flip'])
                # If the object is a moving saw, draw a chain of saw links along its path
                if obj.name == 'saw':
                    if move_dir == 'x':
                        y = start_position[1] - level_frames['saw chain'].get_height() / 2 # middle of the rectangle
                        left, right = int(start_position[0]), int(end_position[0])
                        for x in range(left, right, 20):
                            Sprite((x, y), level_frames['saw chain'], self.allSprites, Z_LAYERS['bg details'])
                    else:
                        x = start_position[0] - level_frames['saw chain'].get_width() / 2 # middle of the rectangle
                        top, bottom = int(start_position[1]), int(end_position[1])
                        for y in range(top, bottom, 20):
                            Sprite((x, y), level_frames['saw chain'], self.allSprites, Z_LAYERS['bg details'])
        #enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth((obj.x, obj.y), level_frames['tooth'], (self.allSprites, self.damageSprites, self.toothSprites), self.collisionSprites)
            if obj.name == 'shell':
                Shell(
                    pos = (obj.x, obj.y), 
                    frames = level_frames['shell'], 
                    groups = (self.allSprites, self.collisionSprites), 
                    reverse = obj.properties['reverse'], 
                    player = self.player, 
                    create_pearl = self.create_pearl )
        #items
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.allSprites, self.itemSprites), self.data)
        # water
        for obj in tmx_map.get_layer_by_name('Water'):
            rows = int(obj.height / TILE_SIZE)
            columns = int(obj.width / TILE_SIZE)
            # Water tiles are stacked based on their row index
            # top row is animated, lower rows are static body tiles 
            for row in range(rows):
                for column in range(columns):
                    x = obj.x + column * TILE_SIZE
                    y = obj.y + row * TILE_SIZE
                    if row == 0:
                        AnimatedSprite((x,y), level_frames['water_top'], self.allSprites, Z_LAYERS['water'])
                    else:
                        Sprite((x,y), level_frames['water_body'], self.allSprites, Z_LAYERS['water'])
            
    def create_pearl(self, pos, direction):
        Pearl(pos, (self.allSprites, self.damageSprites, self.pearlSprites), self.pearl_surf, direction, 150)
        self.pearl_sfx.play()
        
    def pearl_collision(self):
        for sprite in self.collisionSprites:
            sprite = pygame.sprite.spritecollide(sprite, self.pearlSprites, True)
            if sprite:
                ParticleEffectSprite((sprite[0].rect.center), self.particle_frames, self.allSprites)
            
    def hit_collision(self):
        for sprite in self.damageSprites:
            if sprite.rect.colliderect(self.player.hitboxRect):
                self.player.get_damage()
                
                if not self.damage_sfx_timer.active:
                    self.damage_sfx.play()
                    self.damage_sfx_timer.activate()
                if hasattr(sprite, 'pearl'):
                    sprite.kill()
                    ParticleEffectSprite((sprite.rect.center), self.particle_frames, self.allSprites)
    
    def item_collision(self):
        if self.itemSprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.itemSprites, True)
            if item_sprites:
                item_sprites[0].activate()
                ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames, self.allSprites)
                self.coin_sfx.play()
                
    def attack_collision(self):
        for target in self.pearlSprites.sprites() + self.toothSprites.sprites():
            # Enemies that are hit during the player's attack animation and in the correct direction will "reverse"
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or \
                            self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
                target.reverse()
    
    def check_constraint(self): # so the player doesn't go out of bounds
        # constraining the player in the left and right direction
        if self.player.hitboxRect.left <= 0:
            self.player.hitboxRect.left = 0
        if self.player.hitboxRect.right >= self.level_width:
            self.player.hitboxRect.right = self.level_width
        
        # bottom constraints
        # This prevents the player from going off-screen or below the map
        if self.player.hitboxRect.bottom > self.level_bottom:
            self.switch_stage('overworld', -1) # reset or fail level
            
        # player finishes level / passes flag
        if self.player.hitboxRect.colliderect(self.level_finish_rect):
            self.switch_stage('overworld', self.level_unlock)
        
    def run(self, dt): # just calling all necessary functions
        self.damage_sfx_timer.update()
        self.displayWindow.fill('black')
        
        self.allSprites.update(dt)
        self.pearl_collision()
        self.hit_collision()
        self.item_collision()
        self.attack_collision()
        self.check_constraint()
        
        self.allSprites.draw(self.player.hitboxRect.center, dt) # Draw everything relative to player's position