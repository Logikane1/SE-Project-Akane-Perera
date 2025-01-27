from gameSettings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.offset = vector()
        
    def draw(self, target_position):
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2) # creating the offset for the screen that follows the player 
        for sprite in self: # returns all sprites inside of it
            offset_position = sprite.rect.topleft + self.offset
            self.displaySurface.blit(sprite.image, offset_position)