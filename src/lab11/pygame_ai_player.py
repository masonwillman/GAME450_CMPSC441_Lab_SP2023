
# Imports needed for the classes
import random
from lab11.turn_combat import CombatPlayer

""" Create PyGameAIPlayer class here"""

# Class for the AI player
class PyGameAIPlayer:
    
    # Constructor that sets the current_city to 0
    def __init__(self):
        self.current_city = 0
        pass
    
    # method that makes the AI player select an action
    def selectAction(self):
        # we increment the city by 1 and do modulos 10 to prevent going over 9
        self.current_city = (self.current_city + 1) % 10
        # we return the city we want to go to
        return ord(str(self.current_city))
    
    pass


""" Create PyGameAICombatPlayer class here"""

# Class for the AI Combat Player
class PyGameAICombatPlayer(CombatPlayer):
    
    # Constructor for the Combat Player
    def __init__(self, name):
        super().__init__(name)

    # Similar to the computer player, the AI will select a random weapon
    def weapon_selecting_strategy(self):
        # Pick a random number between 1-3 and subtract 1 to stay within weapon index 
        self.weapon = random.randint(1, 3) - 1
        # Return the weapon
        return self.weapon
    
    pass
