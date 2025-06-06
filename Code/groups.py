from gameSettings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, bg_tile = None):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.offset = vector()
        self.width, self.height = width, height
        
    def draw(self, target_position):
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2) # creating the offset for the screen that follows the player 
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)
        
    
    
        for sprite in sorted(self, key = lambda sprite: sprite.z): # returns all sprites inside of it / anything drawn before this for loop is in the background (easy to make sky here)
            offset_position = sprite.rect.topleft + self.offset
            self.displaySurface.blit(sprite.image, offset_position)