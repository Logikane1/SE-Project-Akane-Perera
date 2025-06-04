from gameSettings import * 
from random import choice

class Tooth(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.z = Z_LAYERS['main']
        
        self.direction = choice((-1,1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        
    def update(self,dt):
        
        #animate
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]