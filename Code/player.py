from gameSettings import *
from gameTimer import Timer
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semicollision_sprites):
        super().__init__(groups)
        
        self.image = pygame.image.load(join('Graphics', 'player', 'idle', '0.png'))
        
        self.rect = self.image.get_frect(topleft = pos)
        self.previousRect = self.rect.copy
        
        self.direction = vector()
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jumpHeight = 900
        
        self.collision_sprites = collision_sprites
        self.semicollision_sprites = semicollision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None
        
        self.timers = {
            'wall jump': Timer(300),
            'wall slide': Timer(200),
            'platform fall': Timer(250)
        }
    
    def input(self):
        keys = pygame.key.get_pressed()
        inputVector = vector(0,0)
        if not self.timers['wall jump'].active:
            if keys[pygame.K_d]:
                inputVector.x += 1
            if keys[pygame.K_a]:
                inputVector.x -= 1
            if keys[pygame.K_s]:
                self.timers['platform fall'].activate()
            self.direction.x = inputVector.normalize().x if inputVector else inputVector.x
        
        if keys[pygame.K_SPACE]:
            self.jump = True
            
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide'].active:
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        
        self.collision('vertical')
        self.semiCollision()
        
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jumpHeight
                self.timers['wall slide'].activate()
                self.rect.bottom -= 1
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jumpHeight
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False
            
    def platformMoving(self, dt):
        if self.platform:
            self.rect.topleft += self.platform.direction * self.platform.speed * dt # makes it so player moves along with a moving platform its standing on
    
    def checkContact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width,2))
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4),(2,self.rect.height / 2))
        left_rect  = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4),(2,self.rect.height / 2))
        
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semicollide_rects = [sprite.rect for sprite in self.semicollision_sprites]
        
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semicollide_rects) >= 0 and self.direction.y >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left']  = True if left_rect.collidelist(collide_rects) >= 0 else False
        
        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semicollision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
            
    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect): # checks the collision between the sprite rectangle and the rectangle of the player
                if axis == 'horizontal':
                    if self.rect.left <= sprite.rect.right and self.previousRect.left >= sprite.previousRect.right:
                        self.rect.left = sprite.rect.right
                        
                    if self.rect.right >= sprite.rect.left and self.previousRect.right <= sprite.previousRect.left:
                        self.rect.right = sprite.rect.left
                else:  # vertical
                    if self.rect.top <= sprite.rect.bottom and self.previousRect.top >= sprite.previousRect.bottom:
                        self.rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.rect.top += 6
                        
                    if self.rect.bottom >= sprite.rect.top and self.previousRect.bottom <= sprite.previousRect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    
    def semiCollision(self):
        if not self.timers['platform fall'].active:
            for sprite in self.semicollision_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.rect.bottom >= sprite.rect.top and int(self.previousRect.bottom) <= sprite.previousRect.top:
                        self.rect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0
                    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
    
    def update(self, dt):
        self.previousRect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.platformMoving(dt)
        self.checkContact()