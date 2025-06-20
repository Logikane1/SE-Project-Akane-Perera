from gameSettings import *
from sprites import AnimatedSprite
from random import randint
from gameTimer import Timer

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group() # Group to manage all UI sprite objects
        self.font = font
        
        # health / hearts
        self.heart_frames = frames['heart'] # List of heart animation frames (images)
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 5 # Space between hearts
        
        # coins
        self.coin_amount = 0
        self.coin_timer = Timer(1000) # Timer to control how long coin display stays visible (1 second)
        self.coin_surf = frames['coin']
        
        
    
    def create_hearts(self, amount):
        for sprite in self.sprites:
            sprite.kill()
            
        for heart in range(amount): # Calculate x position with padding, y fixed at 10 pixels from top
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x,y), self.heart_frames, self.sprites) # Create a new Heart sprite and add it to the group
    
    def display_text(self):
        if self.coin_timer.active:
            text_surf = self.font.render(str(self.coin_amount), False, '#333a3d')
            text_rect = text_surf.get_frect(topleft = (16, 34))
            self.display_surface.blit(text_surf, text_rect)
            
            coin_rect = self.coin_surf.get_frect(center = text_rect.bottomleft)
            self.display_surface.blit(self.coin_surf, coin_rect)
        
    def show_coins(self, amount):
        self.coin_amount = amount
        self.coin_timer.activate()
    
    def update(self, dt):
        self.coin_timer.update()
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)
        self.display_text()
            
class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False  # Whether the heart is currently animating
        
    def animate(self, dt): # Animate the heart by cycling through its frames based on delta time.
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active =False
            self.frame_index = 0
    
    def update(self, dt):
        if self.active:
            self.animate(dt)
        else:
            if randint(0, 2000) == 1: # randomly activate the animation sometimes to add a lively effect.
                self.active = True