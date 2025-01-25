from gameSettings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None):
        super().__init__(groups)
        self.image = surf
        self.image.fill('white')
        self.rect = self.image.get_frect(topleft = pos) 
        self.previousRect = self.rect.copy()
        
class MovingSprite(Sprite):
    def __init__(self, groups, start_position, end_position, move_dir, speed):
        surf = pygame.Surface((200, 50))
        super().__init__(start_position, surf, groups)
        self.rect.center = start_position
        self.start_position = start_position
        self.end_position = end_position
        
        #movement
        self.speed = speed
        self.direction = vector(1,0) if move_dir == 'x' else vector(0,1)
        self.move_dir = move_dir
        
    def checkBorder(self): # keeps platform in the rectangle of its movement 
        if self.move_dir == 'x': # for platforms moving horizontally
            if self.rect.right >= self.end_position[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_position[0]
            if self.rect.left <= self.start_position[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_position[0]
        else:
            if self.rect.bottom >= self.end_position[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_position[1]
            if self.rect.top <= self.start_position[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_position[1]
    
    def update(self, dt):
        self.previousRect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.checkBorder()
        
        