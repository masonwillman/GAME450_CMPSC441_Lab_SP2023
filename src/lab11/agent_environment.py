import sys
import pygame
import random
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, get_combat_bg
from pygame_ai_player import PyGameAIPlayer

from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab2.cities_n_routes import get_randomly_spread_cities, get_routes

from lab7.ga_cities import game_fitness, setup_GA, solution_to_cities 
from lab3.travel_cost import get_route_cost
# from lab11.text_to_image import create_image
import numpy as np



pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


def get_landscape_surface(size):
    # Now stores the elevation
    elevation, landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    # Now returns the elevation
    return elevation, pygame_surface


def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])


class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes


if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_speed = 1
    player_path = "assets/player.png"
    opponent_path = "assets/opponent.png"

# Implementation of New A.I. Componenet (text-to-image generation) ##########################################################################################################################3

    prompt = input("What would you like the player to be? ")
    print(prompt)

    # create_image(prompt, player_path)

    prompt = input("What would you like the opponent to be? ")
    print(prompt)

    # create_image(prompt, opponent_path)

###########################################################################################################################################

    screen = setup_window(width, height, "Game World Gen Practice")

    # Gets the landscape and correct elevation
    elevation, landscape_surface = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)

    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    cities = get_randomly_spread_cities(size, len(city_names))

    # Implementation of GA ###########################################################################################
    
    # Gets the correct elevation for the fitness function    
    elevation = np.array(elevation)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())

    # Sets up the fitness function and GA
    fitness = lambda cities, idx: game_fitness(
        cities, idx, elevation, size
    )
    fitness_function, ga_instance = setup_GA(fitness, len(city_names), size)

    # Runs the GA to optimize the parameters
    ga_instance.run()

    # Gets the solution from the GA
    cities = ga_instance.best_solution()[0]
    cities = solution_to_cities(cities, size)

    #################################################################################################################    

    # Implementation of route cost based on terrain #################################################################
    
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:10]
    
    game_map = pygame.surfarray.array3d(landscape_surface);

    route_coordinates = routes

    costs = []

    for route, route_coordinate in zip(routes, route_coordinates):
        print(f'Cost between {route[0]} and {route[1]}: {get_route_cost(route_coordinate, game_map) / 1000}')
        costs.append(get_route_cost(route_coordinate, game_map) / 1000)

    #################################################################################################################

    player_sprite = Sprite(player_path, cities[start_city])

    player = PyGameHumanPlayer()

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""

    # Code to replace human player with AI player
    # player = PyGameAIPlayer();

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )

    while True:
        action = player.selectAction(state, route_coordinates, cities, costs)
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                start = cities[state.current_city]
                state.destination_city = int(chr(action))
                destination = cities[state.destination_city]
                player_sprite.set_location(cities[state.current_city])
                state.travelling = True
                print(
                    "Travelling from", state.current_city, "to", state.destination_city
                )

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)

        # Implementation of player losing if all money is gone ##########################################################################################################      
        if player.gameOver:
            print('You used all your money traveling...you lose.')
            break
        ###########################################################################################################      

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city
        
        # Implmentation of Combat giving money and game over via combat loss##########################################################################################################      
        if state.encounter_event:
            # Returns the currentGame object
            currentGame = run_pygame_combat(combat_surface, screen, player_sprite)
            # check to see if we did not lose
            if not currentGame.lose:
                # Rewards money or does not based on the outcome
                if currentGame.money == 0:
                    print("Since there are a draw, you did not earn money")
                else:
                    player.money = player.money + currentGame.money
                    print ("Since you won, you gained ", currentGame.money)
                    print ("Your total is ", player.money)
            # If we lost, exit the game
            else:
                print("You lost combat. Game Over.")
                sys.exit(0)
            
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        ###########################################################################################################      

        pygame.display.update()

        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break
