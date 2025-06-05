# no pygame needed
class Data:
    def __init__(self, ui):
        self.ui = ui
        self.coins = 0
        self._health = 5 # private attribute
        self.ui.create_hearts(self._health)
        
    @property # getter
    def health(self): # health and _health are the same to outside file, but can now be treated seperately in the Data file
        return self._health
    
    @health.setter # setter
    def health(self, value):
        self._health = value
        self.ui.create_hearts(value)