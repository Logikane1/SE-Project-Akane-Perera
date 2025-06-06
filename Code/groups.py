from gameSettings import *
from sprites import Sprite

class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, clouds, horizon_line, bg_tile = None, top_limit = 0):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.offset = vector()
        self.width, self.height = width * TILE_SIZE, height * TILE_SIZE
        self.borders = {
            'left' : 0,
            'right' : -self.width + WINDOW_WIDTH,
            'bottom' : -self.height + WINDOW_HEIGHT,
            'top' : top_limit}
        self.sky = not bg_tile
        self.horizon_line = horizon_line
        
        if bg_tile:
            for column in range(width):
                for row in range(-int(top_limit / TILE_SIZE) - 1, height):
                    x, y = column * TILE_SIZE, row * TILE_SIZE
                    Sprite((x,y), bg_tile, self, -1)
        else: #sky
            self.large_cloud = clouds['large']
            self.small_clouds = clouds['small']
    
    def camera_constraint(self):
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']
        
    def draw_sky(self):
        self.displaySurface.fill('#ddc6a1')
        horizon_pos = self.horizon_line + self.offset.y
        
        sea_rect = pygame.FRect(0, horizon_pos, WINDOW_WIDTH, WINDOW_HEIGHT - horizon_pos)
        pygame.draw.rect(self.displaySurface, '#92a9ce', sea_rect)
        
        #horizon line
        pygame.draw.line(self.displaySurface, '#fcf4f4', (0, horizon_pos), (WINDOW_WIDTH, horizon_pos), 4)
        
        
    def draw(self, target_position):
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2) # creating the offset for the screen that follows the player 
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)
        self.camera_constraint()
        
        if self.sky:
            self.draw_sky()
        
        for sprite in sorted(self, key = lambda sprite: sprite.z): # returns all sprites inside of it / anything drawn before this for loop is in the background (easy to make sky here)
            offset_position = sprite.rect.topleft + self.offset
            self.displaySurface.blit(sprite.image, offset_position)