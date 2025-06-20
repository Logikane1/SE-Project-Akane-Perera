from gameSettings import *
from sprites import Sprite, Cloud
from random import choice, randint
from gameTimer import Timer

class WorldSprites(pygame.sprite.Group):
    def __init__(self, data):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.data = data
        self.offset = vector()
    
    def draw(self, target_position):
        # Adjust the camera offset based on the player's position
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)
        
        # Draw background sprites (like terrain paths or background decorations)
        for sprite in sorted(self, key = lambda sprite: sprite.z):
            if sprite.z < Z_LAYERS['main']:
                if sprite.z == Z_LAYERS['path']:
                    # Only draw path tiles for levels that have been unlocked
                    if sprite.level <= self.data.unlocked_level:
                        self.displaySurface.blit(sprite.image, sprite.rect.topleft + self.offset)
                else:
                    self.displaySurface.blit(sprite.image, sprite.rect.topleft + self.offset)
                    
        # Draw sprites at the 'main' z-layer, sorted by their vertical position for depth effect
        for sprite in sorted(self, key = lambda sprite: sprite.rect.centery):
            if sprite.z == Z_LAYERS['main']:
                if hasattr(sprite, 'icon'):
                    # Offset upward for icons
                    self.displaySurface.blit(sprite.image, sprite.rect.topleft + self.offset + vector(0, -28))
                else:
                    self.displaySurface.blit(sprite.image, sprite.rect.topleft + self.offset)
        
class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, clouds, horizon_line, bg_tile = None, top_limit = 0):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.offset = vector()
        self.width, self.height = width * TILE_SIZE, height * TILE_SIZE
        # Define camera boundaries
        self.borders = {
            'left' : 0,
            'right' : -self.width + WINDOW_WIDTH,
            'bottom' : -self.height + WINDOW_HEIGHT,
            'top' : top_limit}
        self.sky = not bg_tile # If there's no bg tile, we draw a dynamic sky instead
        self.horizon_line = horizon_line
        
        if bg_tile:
            # Fill the level with a repeating background tile
            for column in range(width):
                for row in range(-int(top_limit / TILE_SIZE) - 1, height):
                    x, y = column * TILE_SIZE, row * TILE_SIZE
                    Sprite((x,y), bg_tile, self, -1)
        else: # Set up dynamic cloud sky
            self.large_cloud = clouds['large']
            self.small_clouds = clouds['small']
            self.cloud_direction = -1
            
            #large cloud
            self.large_cloud_speed = 50
            self.large_cloud_x = 0
            self.large_cloud_tiles = int(self.width / self.large_cloud.get_width()) + 2
            self.large_cloud_width, self.large_cloud_height = self.large_cloud.get_size()
            
            #small cloud
            #timer that makes a cloud every 2.5 seconds
            self.cloud_timer = Timer(2500, self.create_cloud, True)
            self.cloud_timer.activate()
            # Pre-fill sky with small clouds at random positions
            for cloud in range(20):
                pos = (randint(0, self.width),randint(self.borders['top'], self.horizon_line))
                surf = choice(self.small_clouds)
                Cloud(pos, surf, self)
    
    def camera_constraint(self):
        # Clamp the offset values to keep the camera inside the map boundaries
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']
        
    def draw_sky(self):
        # Fill background with sky color
        self.displaySurface.fill("#FFD0AA")
        horizon_pos = self.horizon_line + self.offset.y
        # Draw ocean below horizon
        sea_rect = pygame.FRect(0, horizon_pos, WINDOW_WIDTH, WINDOW_HEIGHT - horizon_pos)
        pygame.draw.rect(self.displaySurface, '#92a9ce', sea_rect)
        
        #horizon line
        pygame.draw.line(self.displaySurface, '#fcf4f4', (0, horizon_pos), (WINDOW_WIDTH, horizon_pos), 4)
        
    def draw_large_cloud(self, dt):
        # Scroll large clouds horizontally for animation effect
        self.large_cloud_x +=  self.cloud_direction * self.large_cloud_speed * dt
        if self.large_cloud_x <=-self.large_cloud_width: # if one cloud has fully exied the screen, animation will reset, making for a seamless infinite loop
            self.large_cloud_x = 0 
            
        for cloud in range(self.large_cloud_tiles):
            left = self.large_cloud_x + self.large_cloud_width * cloud + self.offset.x
            top = self.horizon_line - self.large_cloud_height + self.offset.y
            self.displaySurface.blit(self.large_cloud, (left,top))
        
    def create_cloud(self):
        # Spawn a small cloud just outside the right side of the map
        pos = (randint(self.width + 500, self.width + 600),randint(self.borders['top'], self.horizon_line))
        surf = choice(self.small_clouds)
        Cloud(pos, surf, self)
        
    def draw(self, target_position, dt):
        # Update cloud timer and calculate new camera offset
        self.cloud_timer.update()
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2) # creating the offset for the screen that follows the player 
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)
        self.camera_constraint()
        # If using dynamic sky, draw it before sprites
        if self.sky:
            self.draw_sky()
            self.draw_large_cloud(dt)
        # Draw all sprites in depth order based on z-layer
        for sprite in sorted(self, key = lambda sprite: sprite.z): # returns all sprites inside of it / anything drawn before this for loop is in the background (easy to make sky here)
            offset_position = sprite.rect.topleft + self.offset
            self.displaySurface.blit(sprite.image, offset_position)