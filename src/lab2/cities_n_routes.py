''' 
Lab 2: Cities and Routes

In the final project, you will need a bunch of cities spread across a map. Here you 
will generate a bunch of cities and all possible routes between them.
'''
import random
import itertools

def get_randomly_spread_cities(size, n_cities):
    """
    > This function takes in the size of the map and the number of cities to be generated 
    and returns a list of cities with their x and y coordinates. The cities are randomly spread
    across the map.
    
    :param size: the size of the map as a tuple of 2 integers (100, 100)
    :param n_cities: The number of cities to generate
    :return: A list of cities with random x and y coordinates.
    """
    # Consider the condition where x size and y size are different

    # import random
    # random.randint()

    # citites = []
    # for i in range(100):
    #   cities.append()
    # return cities

    cities = []
    cord = 0

    for i in range(n_cities):
        cord = (random.randint(0, size[0]), random.randint(0, size[1]))
        cities.append(cord)

    return cities

    pass

def get_routes(city_names):
    """
    It takes a list of cities and returns a list of all possible routes between those cities. 
    Equivalently, all possible routes is just all the possible pairs of the cities. 
    
    :param cities: a list of cities, each of which is a tuple of coordinates
    :return: A list of tuples representing all possible links between cities, 
            each item in the list (a link) represents a route between two cities.
    """

    # import itertools
    # a = ['a', 'b', 'c']
    # for a_combination in itertools.combinations(a, 2):
    #   print(a_combination)

    city_names = itertools.combinations(city_names, 2)

    return city_names 

    pass


# TODO: Fix variable names
if __name__ == '__main__':
    city_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    '''print the cities and routes'''
    cities = get_randomly_spread_cities((100, 200), len(city_names))
    routes = get_routes(city_names)
    print('Cities:')
    for i, city in enumerate(cities):
        print(f'{city_names[i]}: {city}')
    print('Routes:')
    for i, route in enumerate(routes):
        print(f'{i}: {route[0]} to {route[1]}')
