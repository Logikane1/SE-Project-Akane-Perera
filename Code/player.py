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
        
        self.collision_sprites = collision_sprites
    
    def input(self):
        keys = pygame.key.get_pressed()
        inputVector = vector(0,0)
        if keys[pygame.K_d]:
            inputVector.x += 1
        if keys[pygame.K_a]:
            inputVector.x -= 1
        self.direction.x = inputVector.normalize().x if inputVector else inputVector.x
            
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')
        
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