import pygame
pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y = 10, x = 10):
    # y : Vertical position on the screen (default 10 pixels from top).
    # x : Horizontal position on the screen (default 10 pixels from left)
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect) # Draw (blit) the text surface onto the display surface at the debug_rect position
    
    