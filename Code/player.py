from gameSettings import *
from gameTimer import Timer
from os.path import join
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semicollision_sprites, frames, data, attack_sfx, jump_sfx):
        #general setup
        super().__init__(groups)
        self.z = Z_LAYERS['main']
        self.data = data
        
        #image
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]
        
        #rectangles
        self.rect = self.image.get_frect(topleft = pos)
        self.hitboxRect = self.rect.inflate(-76, -36)
        self.previousRect = self.hitboxRect.copy()
        
        #movement
        self.direction = vector()
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jumpHeight = 700
        self.attacking = False 
        
        #collisions
        self.collision_sprites = collision_sprites
        self.semicollision_sprites = semicollision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None
        
        #iframes
        self.invincible = False
        
        #timers
        self.timers = {
            'wall jump': Timer(300),
            'wall slide': Timer(200),
            'platform fall': Timer(100),
            'attack cooldown' : Timer(500),
            'hit': Timer(600, self.end_invincibility)
        }
        
        #player audio
        self.attack_sfx = attack_sfx
        self.jump_sfx = jump_sfx
        self.jump_sfx.set_volume(0.1)
        
    def input(self):
        # basic movement
        keys = pygame.key.get_pressed()
        inputVector = vector(0,0)
        if not self.timers['wall jump'].active:
            
            if keys[pygame.K_d]:
                inputVector.x += 1
                self.facing_right = True
            
            if keys[pygame.K_a]:
                inputVector.x -= 1
                self.facing_right = False
            
            if keys[pygame.K_s]:
                self.timers['platform fall'].activate()
                
            if keys[pygame.K_l]:
                self.attack()
            
            self.direction.x = inputVector.normalize().x if inputVector else inputVector.x
        
        if keys[pygame.K_SPACE]:
            self.jump = True
            
    def attack(self):
        # Trigger an attack if cooldown is not active
        if not self.timers['attack cooldown'].active:
            self.attacking = True
            self.frame_index = 0
            self.timers['attack cooldown'].activate()
            self.attack_sfx.play()
            
    def move(self, dt):
        # Handle horizontal movement and collision
        self.hitboxRect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        # Handle gravity and wall sliding
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide'].active:
            self.direction.y = 0
            self.hitboxRect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.hitboxRect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        
        # Jumping mechanics (ground + wall jump)
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jumpHeight
                self.timers['wall slide'].activate()
                self.hitboxRect.bottom -= 1
                self.jump_sfx.play()
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jumpHeight
                self.direction.x = 1 if self.on_surface['left'] else -1
                self.jump_sfx.play()
            self.jump = False
        
        self.collision('vertical')
        self.semiCollision()    
        self.rect.center = self.hitboxRect.center
            
    def platformMoving(self, dt):
        # Follow moving platform if standing on one
        if self.platform:
            self.hitboxRect.topleft += self.platform.direction * self.platform.speed * dt # makes it so player moves along with a moving platform its standing on
    
    def end_invincibility(self): # Callback for when invincibility ends
        self.invincible = False
    
    def checkContact(self): # Create small rectangles for each side to detect contact
        floor_rect = pygame.Rect(self.hitboxRect.bottomleft,(self.hitboxRect.width,2))
        right_rect = pygame.Rect(self.hitboxRect.topright + vector(0, self.hitboxRect.height / 4),(2,self.hitboxRect.height / 2))
        left_rect  = pygame.Rect(self.hitboxRect.topleft + vector(-2, self.hitboxRect.height / 4),(2,self.hitboxRect.height / 2))
        
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semicollide_rects = [sprite.rect for sprite in self.semicollision_sprites]
        
        # Check each direction for collisions
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semicollide_rects) >= 0 and self.direction.y >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left']  = True if left_rect.collidelist(collide_rects) >= 0 else False
        
        # Check if player is on a moving platform
        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semicollision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
            
    def collision(self, axis): # collision handling for both horizontal and vertical movement
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitboxRect): # checks the collision between the sprite rectangle and the rectangle of the player
                if axis == 'horizontal':
                    if self.hitboxRect.left <= sprite.rect.right and int(self.previousRect.left) >= int(sprite.previousRect.right):
                        self.hitboxRect.left = sprite.rect.right
                        
                    if self.hitboxRect.right >= sprite.rect.left and int(self.previousRect.right) <= int(sprite.previousRect.left):
                        self.hitboxRect.right = sprite.rect.left
                else:  # vertical
                    if self.hitboxRect.top <= sprite.rect.bottom and int(self.previousRect.top) >= int(sprite.previousRect.bottom):
                        self.hitboxRect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.hitboxRect.top += 6
                        
                    if self.hitboxRect.bottom >= sprite.rect.top and int(self.previousRect.bottom) <= int(sprite.previousRect.top):
                        self.hitboxRect.bottom = sprite.rect.top
                    self.direction.y = 0
                    
    def semiCollision(self): # Collisions with one-way platforms (fall-through)
        if not self.timers['platform fall'].active:
            for sprite in self.semicollision_sprites:
                if sprite.rect.colliderect(self.hitboxRect):
                    if self.hitboxRect.bottom >= sprite.rect.top and int(self.previousRect.bottom) <= sprite.previousRect.top:
                        self.hitboxRect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0
                    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
    
    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.state == 'attack' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'idle'
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        
        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False
        
    def get_state(self): # Determine current state based on movement and collisions
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'attack'
            else:
                self.state = 'idle' if self.direction.x == 0 else 'running'
        else:
            if self.attacking:
                self.state = 'air_attack'
            else:
                if any((self.on_surface['left'], self.on_surface['right'])):
                    self.state = 'wall'
                else:
                    self.state = 'jump' if self.direction.y < 0 else 'fall'
    
    def get_damage(self): # Take damage and activate invincibility
        if not self.invincible:
            self.data.health -= 1
            self.invincible = True
            self.timers['hit'].activate()
    
    def flicker(self): # Flicker effect during invincibility
        if self.timers['hit'].active and sin(pygame.time.get_ticks() / 25) >= 0 : # the sin curve will infintely change between 1 and -1, allowing for a 'flickering' effect
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface() # gives silhouette of the player
            white_surf.set_colorkey('black')
            self.image = white_surf
    
    def update(self, dt):
        #general updating
        self.previousRect = self.hitboxRect.copy()
        self.update_timers()
        #input updating
        self.input()
        self.move(dt)
        self.platformMoving(dt)
        self.checkContact()
        #animating
        self.get_state()
        self.animate(dt)
        self.flicker()