import pygame
from Configuration import *
from ModLevel import Level

pygame.init()
time = pygame.time.Clock()

displayWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Archon")

run = True
level = Level(displayWindow)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run == False
                
    pygame.display.flip()
    time.tick(60)
    
pygame.quit()
    