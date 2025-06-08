from gameSettings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from debug import debug
from ui import UI
from overworld import Overworld

class Game:
    def __init__(self):
        pygame.init()
        self.displayWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("THE ARCHON")
        self.clock = pygame.time.Clock()
        self.importAssets()
        
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui) 
        self.tmx_maps = {
            0: load_pygame(join('Data', 'Levels', '0.tmx')),
            1: load_pygame(join('Data', 'Levels', '1.tmx')),
            2: load_pygame(join('Data', 'Levels', '2.tmx')),
            3: load_pygame(join('Data', 'Levels', '3.tmx')),
            4: load_pygame(join('Data', 'Levels', '4.tmx')),
            5: load_pygame(join('Data', 'Levels', '5.tmx')),
            }
        self.tmx_overworld = load_pygame(join('Data', 'Overworld', 'overworld.tmx'))
        self.currentStage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        
    def switch_stage(self, target, unlock = 0):
        if target == 'level':
            self.currentStage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
            
        else: #overworld
            if unlock > 0:
                self.data.unlocked_level = unlock
            else:
                self.data.health -= 1
            self.currentStage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
            
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
            'bg_tiles' : importFolderDict('Graphics', 'level', 'bg', 'tiles'),
            'cloud_small' :importFolder('Graphics', 'level', 'clouds', 'small'),
            'cloud_large' : importImage('Graphics', 'level', 'clouds', 'large_cloud')
        }
        
        self.font = pygame.font.Font(join('Graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart' : importFolder('Graphics', 'ui', 'heart'),
            'coin' : importImage('Graphics', 'ui', 'coin')
        }

        self.overworld_frames ={
            'palms' : importFolder('Graphics', 'overworld', 'palm'),
            'water' : importFolder('Graphics', 'overworld', 'water'),
            'path' : importFolderDict('Graphics', 'overworld', 'path'),
            'icon' : importSubfolder('Graphics', 'overworld', 'icons'),
        }
        
        self.audio_files = {
            'coin': pygame.mixer.Sound(join('Audio', 'coin.wav')),
            'jump': pygame.mixer.Sound(join('Audio', 'jump.wav')),
            'attack': pygame.mixer.Sound(join('Audio', 'attack.wav')),
            'damage': pygame.mixer.Sound(join('Audio', 'damage.wav')),
            'pearl': pygame.mixer.Sound(join('Audio', 'pearl.wav')),
            'hit': pygame.mixer.Sound(join('Audio', 'hit.wav')),
            }
        
    def check_game_over(self):
        if self.data.health <= 0:
            pygame.quit()
            sys.exit()
            
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            max_dt = 0.005
            dt = min(dt, max_dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.check_game_over()
            self.currentStage.run(dt)
            self.ui.update(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()