from gameSettings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((39, 49))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft = pos)
        
        self.direction = vector()
        self.speed = 0.5
    
    def input(self):
        keys = pygame.key.get_pressed()
        inputVector = vector(0,0)
        if keys[pygame.K_d]:
            inputVector.x += 1
        if keys[pygame.K_a]:
            inputVector.x -= 1
        self.direction = inputVector.normalize() if inputVector else inputVector
            
    def move(self):
        self.rect.topleft += self.direction * self.speed
    
    def update(self):
        self.input()
        self.move()