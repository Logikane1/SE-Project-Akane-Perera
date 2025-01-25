from pygame.time import get_ticks

class Timer:
    def __init__(self, duration, func = None, repeat = False):
        self.duration = duration
        self.func = func
        self.startTime = 0
        self.active = False
        self.repeat = repeat
    
    def activate(self):
        self.active = True
        self.startTime = get_ticks()
    
    def deactivate(self):
        self.active = False
        self.startTime = 0
        if self.repeat:
            self.activate()
            
    def update(self):
        current_time = get_ticks()
        if current_time - self.startTime >= self.duration:
            if self.func and self.startTime != 0:
                self.func
            self.deactivate