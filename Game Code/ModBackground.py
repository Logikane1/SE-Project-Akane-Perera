import pygame
from Configuration import *


class Background():
    def __init__(self):
        self.backgroundImage = pygame.image.load(SPRITESHEET_PATH).convert()
        self.backgroundImage = pygame.transform.scale(self.backgroundImage, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
    def draw(self, displayWindow):
        displayWindow.blit(self.backgroundImage,(0, 0))