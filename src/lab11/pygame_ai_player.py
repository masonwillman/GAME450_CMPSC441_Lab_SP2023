
# Imports needed for the classes
import random
import pygame
from lab11.turn_combat import CombatPlayer

""" Create PyGameAIPlayer class here"""


class PyGameAIPlayer:
    
    def __init__(self):
        self.nextcity = 0
        pass

    def selectAction(self, state):
        self.nextcity += 1
        return self.nextcity
    
    pass


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer(CombatPlayer):
    
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        self.weapon = random.randint(1, 3)
        return self.weapon
    
    pass
