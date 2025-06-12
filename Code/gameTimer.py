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
        self.startTime = get_ticks() # Pygame's current time in ms since program start
    
    def deactivate(self): # stops timer
        self.active = False
        self.startTime = 0
        if self.repeat: # If repeat is True, reactivates the timer immediately
            self.activate()
            
    def update(self): # 
        current_time = get_ticks()
        # Only proceed if the timer is active and has been started
        if current_time - self.startTime >= self.duration:
            # Call the function if assigned and timer was properly started
            if self.func and self.startTime != 0:
                self.func()
            self.deactivate()