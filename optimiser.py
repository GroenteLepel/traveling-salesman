import copy

import numpy as np
from itertools import combinations

from tour import Tour
from world import World


def optimise(world: World, n_mc_samples: int = -1,
             init_temperature: float = -1, cooling_factor: float = 0.9):
    if init_temperature < 0:
        init_temperature = world.n_cities / 8
    if n_mc_samples < 0:
        n_mc_samples = int(choose(world.n_cities, 2) / 2)
    temperature = init_temperature

    new_sample_found = True
    distances = np.zeros(n_mc_samples)
    cnt = 0

    print("=============")
    print("Starting simulated annealing with variables:")
    print(r"n_samples: {}, T_i: {}, f_c: {}".format(n_mc_samples,
                                                    init_temperature,
                                                    cooling_factor))
    print("==============")
    while new_sample_found:
        new_sample_found = False
        for _ in range(n_mc_samples):
            current_distance = world.tour.distance
            swap = np.random.choice(world.n_cities, size=2, replace=False)
            world.tour.swap_cities(swap[0], swap[1])
            new_distance = world.tour.distance

            if accept(current_distance, new_distance, temperature):
                new_sample_found = True
            else:
                world.tour.swap_cities(swap[0], swap[1])

            distances[_] = world.tour.distance

        world.show(
            r"$T$ = {0:.3f}, avg_dist = {1:.3f}".format(temperature,
                                                        distances.mean())
        )
        temperature *= cooling_factor
    return world


def choose(n, k):
    return np.math.factorial(n) / \
           (np.math.factorial(n - k) * np.math.factorial(k))


def p(tour: Tour, temperature: float):
    return np.exp(-tour.distance / temperature)


def generate_swaplist(n_cities: int):
    index_list = [x for x in range(n_cities)]
    return list(combinations(index_list, 2))


def accept(old_sample: float, candidate_sample: float, temperature: float):
    diff = candidate_sample - old_sample
    a = np.exp(- diff / temperature)

    if a >= 1:
        return True
    elif np.random.rand() <= a:
        return True
    else:
        return False
