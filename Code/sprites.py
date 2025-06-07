from gameSettings import *
from math import sin, cos, radians
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None, z = Z_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos) 
        self.previousRect = self.rect.copy()
        self.z = z
        
class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z = Z_LAYERS['main'], animation_speed = ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0 # self.frames is going to be a list of surfaces, self.frameindex will allow to pick 1 surface
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed
        
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt # this is to make sure the animations are playing at the same speed on every computer
        self.image = self.frames[int(self.frame_index % len(self.frames))] # after the first line self.frameindex will be a floating point so it needs to be int. Added len(self.frames_index) to limit sel.frame_index so it doesn't exceed self.frames
    
    def update(self, dt):
        self.animate(dt)

class Item(AnimatedSprite):
    def __init__(self, item_type, pos, frames, groups, data):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.item_type = item_type
        self.data = data
        
    def activate(self):
        if self.item_type == 'silver':
            self.data.coins += 1
        if self.item_type == 'gold':
            self.data.coins += 5
        if self.item_type == 'diamond':
            self.data.coins += 20
        if self.item_type == 'skull':
            self.data.coins += 50
        if self.item_type == 'potion':
            self.data.health += 1
        
class ParticleEffectSprite(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.z = Z_LAYERS['fg']
        
    def animate(self, dt): # Plays the animation once then destorys the object
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
        
class MovingSprite(AnimatedSprite):
    def __init__(self, frames, groups, start_position, end_position, move_dir, speed, flip = False):
        super().__init__(start_position, frames, groups)
        if move_dir == 'x':
            self.rect.midleft = start_position
        else:
            self.rect.midtop = start_position
        self.start_position = start_position
        self.end_position = end_position
        
        #movement
        self.moving = True
        self.speed = speed
        self.direction = vector(1,0) if move_dir == 'x' else vector(0,1)
        self.move_dir = move_dir
        
        self.flip = flip
        self.reverse = {'x': False, 'y': False}
        
    def checkBorder(self): # keeps platform in the rectangle of its movement 
        if self.move_dir == 'x': # for platforms moving horizontally
            if self.rect.right >= self.end_position[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_position[0]
            if self.rect.left <= self.start_position[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_position[0]
            self.reverse['x'] = True if self.direction.x < 0 else False
        else:
            if self.rect.bottom >= self.end_position[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_position[1]
            if self.rect.top <= self.start_position[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_position[1]
            self.reverse['y'] = True if self.direction.y >  0 else False
            
    def update(self, dt):
        self.previousRect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.checkBorder()
        self.animate(dt)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.reverse['x'], self.reverse['y'])
            
class Spike(Sprite):
    def __init__(self, pos, surf, groups, radius, speed, start_angle, end_angle, z = Z_LAYERS['main']):
        self.center = pos
        self.radius = radius # acts as the hypotenuse /  is the radius of the spike ball circlular path
        self.speed = speed
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.angle = self.start_angle # a
        self.direction = 1
        self.full_circle = True if self.end_angle == -1 else False
        
        # trigonometry
        y = self.center[1] + sin(radians(self.angle)) * self.radius # y = sin(a) x r
        x = self.center[0] + cos(radians(self.angle)) * self.radius # x = cos(a) x r
        
        super().__init__((x,y), surf, groups, z)
        
    def update(self, dt):
        self.angle += self.direction * self.speed * dt
        
        if not self.full_circle:
            if self.angle >= self.end_angle:
                self.direction = -1
            if self.angle < self.start_angle:
                self.direction = 1
        
        y = self.center[1] + sin(radians(self.angle)) * self.radius
        x = self.center[0] + cos(radians(self.angle)) * self.radius
        self.rect.center = (x,y)
        
class Cloud(Sprite):
    def __init__(self, pos, surf, groups, z = Z_LAYERS['clouds']):
        super().__init__(pos, surf, groups, z)
        self.speed = randint(50, 120)
        self.direction = -1
        self.rect.midbottom = pos
        
    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt
        
        if self.rect.right <= 0:
            self.kill()
            
class Node(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, level, data, paths):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (pos[0]+ TILE_SIZE / 2, pos[1]+ TILE_SIZE / 2))
        self.z = Z_LAYERS['path']
        self.level = level
        self.data = data
        self.paths = paths
        
    def can_move(self, direction):
        if direction in list(self.paths.keys()):
            return True  
        
class Icon(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames):
        super().__init__(groups)
        self.icon = True
        self.path = None
        self.direction = vector()
        self.speed = 400
        
        #image
        self.frames, self.frame_index = frames, 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.z = Z_LAYERS['main']
        
        #rect
        self.rect = self.image.get_frect(center = pos)
        
    def start_move(self, path):
        self.rect.center = path[0]
        self.path = path[1:]
        self.find_path()
    
    def find_path(self): #checks for which direction the player can go in
        if self.path:
            print(self.path)
            if self.rect.centerx == self.path[0][0]: #vertical axis
                self.direction = vector(0, 1 if self.path[0][1] > self.rect.centery else -1) 
            else: #horizontal axis
                self.direction = vector(1 if self.path[0][0] > self.rect.centerx else -1, 0) 
        else:
            self.direction = vector()
            
    def point_collision(self):
        if self.direction.y == 1 and self.rect.centery >= self.path[0][1] or \
            self.direction.y == -1 and self.rect.centery <= self.path[0][1]:
            self.rect.centery = self.path[0][1]
            del self.path[0]
            self.find_path()
            
        if  self.direction.x == 1 and self.rect.centerx >= self.path[0][0] or \
            self.direction.x == -1 and self.rect.centerx <= self.path[0][0]:
            self.rect.centerx = self.path[0][0]
            del self.path[0]
            self.find_path()
            
    def update(self, dt):
        if self.path:
            self.point_collision()
            self.rect.center += self.direction * self.speed * dt