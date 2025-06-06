# no pygame needed
class Data:
    def __init__(self, ui):
        self.ui = ui
        self._coins = 0
        self._health = 5 # private attribute
        self.ui.create_hearts(self._health)
        
        self.unlocked_level = 2
        self.current_level = 0
        
    @property # getter
    def coins(self): # coins and _coins are the same to outside files, but can now be treated seperately in the Data file
        return self._coins
    
    @coins.setter # setter
    def coins(self, value):
        self._coins = value
        if self.coins >= 100:
            self.coins -= 100
            self.health += 1
        self.ui.show_coins(self.coins)
        
    @property # getter
    def health(self): # health and _health are the same to outside files, but can now be treated seperately in the Data file
        return self._health
    
    @health.setter # setter
    def health(self, value):
        self._health = value
        self.ui.create_hearts(value)
