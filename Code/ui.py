from gameSettings import *
from sprites import AnimatedSprite

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font
        
        # health / hearts
        self.heart_frames = frames['heart']
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 5
        self.create_hearts(5)
        
        
        # coins
    
    def create_hearts(self, amount):
        for heart in range(amount):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x,y), self.heart_frames, self.sprites)
    
    def update(self, dt):
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)
            
class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        