from gameSettings import *

class Game:
    def __init__(self):
        pygame.init()
        self.displayWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("THE ARCHON")
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()