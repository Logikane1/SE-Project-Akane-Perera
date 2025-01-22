import pygame
from classlevel import Level

# intialise pygame
pygame.init()
time = pygame.time.Clock()

# window specifics
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540

# generating the window
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Archon")

run = True
level = Level()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                
    pygame.display.flip()
    time.tick(60)  # limits frame rate to 60 fps

pygame.quit()
