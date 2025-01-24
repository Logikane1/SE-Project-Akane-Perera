from gameSettings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

class Game:
    def __init__(self):
        pygame.init()
        self.displayWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("THE ARCHON")
        
        self.tmx_maps = {0: load_pygame(join('Data', 'Levels', 'omni.tmx'))}
        
        self.currentStage = Level(self.tmx_maps[0])
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.currentStage.run()
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()