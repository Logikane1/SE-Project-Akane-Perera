import pygame 
from Configuration import *
from ModSpriteSheet import Spritesheet

idleSprites = [
    (16, 0, 48, 48),
    (80, 0, 48, 48),
    (144, 0, 48, 48),
    (208, 0, 48, 48),
    (272, 0, 48, 48),
    (336, 0, 48, 48),
    (400, 0, 48, 48),
    (464, 0, 48, 48),
    (528, 0, 48, 48),
    (592, 0, 48, 48),
    (656, 0, 48, 48)
]

runSprites = [
    (11, 0, 53, 53),
    (75, 0, 53, 53),
    (139, 0, 53, 53),
    (203, 0, 53, 53),
    (267, 0, 53, 53),
    (331, 0, 53, 53),
    (395, 0, 53, 53),
    (459, 0, 53, 53)
]

attackSprites = [
    (0, 0, 91, 91),
    (91, 0, 91, 91),
    (182, 0, 91, 91),
    (263, 0, 91, 91),
    (344, 0, 91, 91),
    (425, 0, 91, 91),
]



class mainCharacter():
    def __init__(self, position, face_right):
        
        idle_SpriteSheet = Spritesheet(SPRITESHEET_PATH + "/Charcter/Idle/Idle.png", idleSprites)
        run_SpriteSheet = Spritesheet(SPRITESHEET_PATH + "/Character/Running/Run.png", runSprites)
        attack_SpriteSheet = Spritesheet(SPRITESHEET_PATH + "/Character/Attack/Attack.png", attackSprites)
        
    def update(self, level):
        pass
    
    def draw(self, displayWindow):
        pass