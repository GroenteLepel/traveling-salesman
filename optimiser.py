import numpy as np
import time
from itertools import combinations

from tour import Tour
from world import World


def optimise(world: World, n_mc_samples: int, init_temperature:float, cooling_factor: float):
    previous_tour = 0
    temperature = init_temperature
    
    while previous_tour != world.tour:
        previous_tour = world.tour
        
        for _ in range(n_mc_samples):
            swaplist = generate_swaplist(world.n_cities)
            
            current_distance = world.tour.distance
            for swap in swaplist:
                world.tour.swap_cities(swap[0], swap[1])
                new_distance = world.tour.distance
                if accept(current_distance, new_distance, temperature):
                    continue
                else:
                    world.tour.swap_cities(swap[0], swap[1])
        
        temperature *= cooling_factor
            
    return world


def p(tour: Tour, temperature: float):
    return np.exp(-tour.distance / temperature)


def generate_swaplist(n_cities: int):
    index_list = [x for x in range(n_cities)]
    return list(combinations(index_list, 2))


def accept(tour_distance: float, trial_tour_distance: float, temperature: float):
    tour_distrance_difference = trial_tour_distance - tour_distance
    a = np.exp(- tour_distrance_difference / temperature)

    if a >= 1:
        return True
    elif np.random.rand() <= a:
        return True
    else:
        return False