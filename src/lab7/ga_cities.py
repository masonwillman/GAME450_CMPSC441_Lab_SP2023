"""
Lab 7: Realistic Cities 

In this lab you will try to generate realistic cities using a genetic algorithm.
Your cities should not be under water, and should have a realistic distribution across the landscape.
Your cities may also not be on top of mountains or on top of each other.
Create the fitness function for your genetic algorithm, so that it fulfills these criterion
and then use it to generate a population of cities.

Please comment your code in the fitness function to explain how are you making sure each criterion is 
fulfilled. Clearly explain in comments which line of code and variables are used to fulfill each criterion.
"""
import matplotlib.pyplot as plt
import pygad
import numpy as np

import sys
from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / ".." / "..").resolve().absolute()))

from src.lab5.landscape import elevation_to_rgba

# This imports the get elevation function from lab 5
from src.lab5.landscape import get_elevation

# This imports the sqrt function for the distance formula
from math import sqrt

def game_fitness(cities, idx, elevation, size):
    fitness = 0.0001  # Do not return a fitness of 0, it will mess up the algorithm.

    """
    Create your fitness function here to fulfill the following criteria:
    1. The cities should not be under water
    2. The cities should have a realistic distribution across the landscape
    3. The cities may also not be on top of mountains or on top of each other
    """
    # Gets the cordinates for each city
    cords = solution_to_cities(cities, size)  
    # Copies the coordinates to another variable  
    neighbors = cords
    # Goes through each cordinate for each city
    for cord1 in cords:
        # Assigns x1 and y1 the x and y values of the cordinates
        x1 = cord1[0]
        y1 = cord1[1]

        # Properly scales the elevation
        # For example, 0.5 would become 5
        fitscale1 = elevation[x1][y1] * 10
        # Checks to see if the elevation is below 5 (which is checking if the city is under water)
        if fitscale1 < 5:
            # If so, we add our fitness scale factor to the fitness 
            # The lower the elvation, the less the fitness scale factor will be
            fitness += fitscale1
        # Checks to see if the elevation is above 5 (which is checking if the city is on a mountain)
        elif fitscale1 > 5:
            # If so, we add our fitness scale factor to the fitness 
            # The higher the elevation, the lower the scale factor
            # For example, 6 would be 6-10 = -4 * -1 = 4. 9 would be 9-10 = -1 * -1 = 1
            fitness += (fitscale1-10)*-1
        
        for cord2 in neighbors:
            # Assigns x2 and y2 the x and y values of the cordinates of the neighbording cities
            x2 = cord2[0]
            y2 = cord2[1]

            # Calculates the distance of each coordinate using the distance formula
            distance = sqrt(pow((y1-y2), 2) + pow((x1-x2), 2))
            
            # divides the distance by 150 (the max distance), to properly scale it
            # For example, 100/150 = 0.67
            # We do this because each city has 10 neighbors, so the fitness scale for distance must be 
            # less than elevation in order for the priority of each to be the same
            # If each city was 0.5, then 10 * 0.5 would be added or 5. 
            fitscale2 = distance/150
            
            # Checks to see if the distance is less than or greater than the target distance (25)
            if distance < 25:
                # If less than, we add the distance scale factor
                fitness += fitscale2
            elif distance > 25:
                # If greater than, we add the distamce scale factor after recalculation
                # For example, 50 would be 50/150 = 0.33-1 = -0.67 * -1 = 0.67
                fitness += (fitscale2-1)*-1

    # Returns the fitness value after completition        
    return fitness


def setup_GA(fitness_fn, n_cities, size):
    """
    It sets up the genetic algorithm with the given fitness function,
    number of cities, and size of the map

    :param fitness_fn: The fitness function to be used
    :param n_cities: The number of cities in the problem
    :param size: The size of the grid
    :return: The fitness function and the GA instance.
    """
    num_generations = 100
    num_parents_mating = 10

    solutions_per_population = 300
    num_genes = n_cities

    init_range_low = 0
    init_range_high = size[0] * size[1]

    parent_selection_type = "sss"
    keep_parents = 10

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_fn,
        sol_per_pop=solutions_per_population,
        num_genes=num_genes,
        gene_type=int,
        init_range_low=init_range_low,
        init_range_high=init_range_high,
        parent_selection_type=parent_selection_type,
        keep_parents=keep_parents,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes,
    )

    return fitness_fn, ga_instance


def solution_to_cities(solution, size):
    """
    It takes a GA solution and size of the map, and returns the city coordinates
    in the solution.

    :param solution: a solution to GA
    :param size: the size of the grid/map
    :return: The cities are being returned as a list of lists.
    """
    cities = np.array(
        list(map(lambda x: [int(x / size[0]), int(x % size[1])], solution))
    )
    return cities


def show_cities(cities, landscape_pic, cmap="gist_earth"):
    """
    It takes a list of cities and a landscape picture, and plots the cities on top of the landscape

    :param cities: a list of (x, y) tuples
    :param landscape_pic: a 2D array of the landscape
    :param cmap: the color map to use for the landscape picture, defaults to gist_earth (optional)
    """
    cities = np.array(cities)
    plt.imshow(landscape_pic, cmap=cmap)
    plt.plot(cities[:, 1], cities[:, 0], "r.")
    plt.show()


if __name__ == "__main__":
    print("Initial Population")

    size = 100, 100
    n_cities = 10
    elevation = []
    """ initialize elevation here from your previous code"""
    elevation = get_elevation(size)
    # normalize landscape
    elevation = np.array(elevation)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())
    landscape_pic = elevation_to_rgba(elevation)

    # setup fitness function and GA
    fitness = lambda cities, idx: game_fitness(
        cities, idx, elevation=elevation, size=size
    )
    fitness_function, ga_instance = setup_GA(fitness, n_cities, size)

    # Show one of the initial solutions.
    cities = ga_instance.initial_population[0]
    cities = solution_to_cities(cities, size)
    show_cities(cities, landscape_pic)

    # Run the GA to optimize the parameters of the function.
    ga_instance.run()
    ga_instance.plot_fitness()
    print("Final Population")

    # Show the best solution after the GA finishes running.
    cities = ga_instance.best_solution()[0]
    cities_t = solution_to_cities(cities, size)
    plt.imshow(landscape_pic, cmap="gist_earth")
    plt.plot(cities_t[:, 1], cities_t[:, 0], "r.")
    plt.show()
    print(fitness_function(cities, 0))
