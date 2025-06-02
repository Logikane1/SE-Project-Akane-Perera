from gameSettings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.displayWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("THE ARCHON")
        self.clock = pygame.time.Clock()
        self.importAssets()
        
        self.tmx_maps = {0: load_pygame(join('Data', 'Levels', 'omni.tmx'))}
        
        self.currentStage = Level(self.tmx_maps[0], self.level_frames)
        
    def importAssets(self):
        self.level_frames = {
            'floor_spikes' : importFolder('Graphics', 'enemies', 'floor_spikes'),
            'fire_trap' : importFolder('Graphics', 'enemies', 'fire_trap'),
            'dark_trees' : importSubfolder('Graphics', 'level', 'trees'),
            'candle' : importFolder('Graphics', 'level', 'candle'),
            'player' : importSubfolder('Graphics', 'player')
        }


    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            max_dt = 0.005
            dt = min(dt, max_dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.currentStage.run(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()