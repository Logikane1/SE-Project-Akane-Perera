from gameSettings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((39, 49))
        self.image.fill('red')
        
        
        self.rect = self.image.get_frect(topleft = pos)
        self.previousRect = self.rect.copy
        
        self.direction = vector()
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jumpHeight = 900
        
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        
        self.display_surface = pygame.display.get_surface()
    
    def input(self):
        keys = pygame.key.get_pressed()
        inputVector = vector(0,0)
        if keys[pygame.K_d]:
            inputVector.x += 1
        if keys[pygame.K_a]:
            inputVector.x -= 1
        self.direction.x = inputVector.normalize().x if inputVector else inputVector.x
        
        if keys[pygame.K_SPACE]:
            self.jump = True
            
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])):
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        
        self.collision('vertical')
        
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jumpHeight
            elif any((self.on_surface['left'], self.on_surface['right'])):
                self.direction.y = -self.jumpHeight
            self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False
        
        
    def checkContact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width,2))
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4),(2,self.rect.height / 2))
        left_rect  = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4),(2,self.rect.height / 2))
        
        
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left']  = True if left_rect.collidelist(collide_rects) >= 0 else False
        
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
                        
                    if self.rect.bottom >= sprite.rect.top and self.previousRect.bottom <= sprite.previousRect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                
    def update(self, dt):
        self.previousRect = self.rect.copy()
        self.input()
        self.move(dt)
        self.checkContact()