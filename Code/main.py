from gameSettings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from debug import debug
from ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.displayWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("THE ARCHON")
        self.clock = pygame.time.Clock()
        self.importAssets()
        
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui) 
        self.tmx_maps = {0: load_pygame(join('Data', 'Levels', 'omni.tmx'))}
        self.currentStage = Level(self.tmx_maps[0], self.level_frames, self.data)
        
    def importAssets(self):
        self.level_frames = {
            'floor_spikes' : importFolder('Graphics', 'enemies', 'floor_spikes'),
            'fire_trap' : importFolder('Graphics', 'enemies', 'fire_trap'),
            'dark_trees' : importSubfolder('Graphics', 'level', 'trees'),
            'flag' : importFolder('Graphics', 'level', 'flag'),
            'candle' : importFolder('Graphics', 'level', 'candle'),
            'player' : importSubfolder('Graphics', 'player'),
            'saw' : importFolder('Graphics', 'enemies', 'saw', 'animation'),
            'saw chain' : importImage('Graphics', 'enemies', 'saw', 'saw_chain'),
            'helicopter' : importFolder('Graphics', 'level', 'helicopter'),
            'boat' : importFolder('Graphics', 'objects', 'boat'),
            'spike' : importImage('Graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain' : importImage('Graphics' , 'enemies', 'spike_ball', 'spiked_chain'),
            'tooth' : importFolder('Graphics', 'enemies', 'tooth', 'run'),
            'shell' : importSubfolder('Graphics', 'enemies', 'shell'),
            'pearl' : importImage('Graphics', 'enemies', 'bullets', 'pearl'),
            'items' : importSubfolder('Graphics', 'items'),
            'particle' : importFolder('Graphics', 'effects', 'particle'),
            'water_top' : importFolder('Graphics', 'level', 'water', 'top'),
            'water_body' : importImage('Graphics', 'level', 'water', 'body'),
        }
        
        self.font = pygame.font.Font(join('Graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart' : importFolder('Graphics', 'ui', 'heart'),
            'coin' : importImage('Graphics', 'ui', 'coin')
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
            self.ui.update(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()