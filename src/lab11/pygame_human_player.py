import pygame
from lab11.turn_combat import CombatPlayer

# Implmentation of restricting movement between cities without route #####################################################################################################################
# Implmentation of losing money based on route cost #####################################################################################################################
class PyGameHumanPlayer:
    def __init__(self):
        self.money = 500
        self.gameOver = False

    # IMPLMENT THE ROUTES IN BOTH DIRECTIONS
    def selectAction(self, state, route_coordinates, cities, costs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                    # Goes through each coordinate
                    for i in range(len(route_coordinates)):

                        # Gets the variables that will be compared
                        city1 = route_coordinates[i][0]
                        city2 = route_coordinates[i][1]

                        current = cities[state.current_city]
                        if ord("0") <= event.key <= ord("9"):
                            destination = cities[event.key-48]
                        else:
                            break;

                        # Checks to see if the current city and destination match those in the route
                        if (city1 == current).all() and (city2 == destination).all():

                            # If do, subtract the cost from money, checking if we are out of money
                            self.money = self.money - costs[i]
                            print("You have ", self.money, " left.")

                            if (self.money <= 0):
                                self.gameOver = True

                            return event.key
                    
                        # Checks to see if the current city and destination match those in the route
                        if (city1 == destination).all() and (city2 == current).all():

                            # If do, subtract the cost from money, checking if we are out of money
                            self.money = self.money - costs[i]
                            print("You have ", self.money, " left.")
                            
                            if (self.money <= 0):
                                self.gameOver = True

                            return event.key
        
        return ord(str(state.current_city))  # Not a safe operation for >10 cities
######################################################################################################################

class PyGameHumanCombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [ord("s"), ord("a"), ord("f")]:
                        choice = {ord("s"): 1, ord("a"): 2, ord("f"): 3}[event.key]
                        self.weapon = choice - 1
                        return self.weapon
