import pygame
from Configuration import *
from ModLevel import Level

pygame.init()
time = pygame.time.Clock()

displayWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Archon")

is_running = True
level = Level(displayWindow)

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_runningrun = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
    
    level.update()
    level.draw()
    
    pygame.display.flip()
    time.tick(60)
    
pygame.quit()
    