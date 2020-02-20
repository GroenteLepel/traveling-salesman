import copy
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt

from tour import Tour
from world import World


def optimise(world: World):
    sa_world = sa_solution(world)
    world = kruus_druut_hoalen(sa_world)
    return world


def sa_solution(world: World, n_mc_samples: int = -1, neighbourhood: int = 2,
                init_temperature: float = -1, cooling_factor: float = 0.9, rising_mc_factor: float = 1,
                show_steps: bool = False):
    if init_temperature < 0:
        init_temperature = world.n_cities / 8
    if n_mc_samples < 0:
        n_mc_samples = int(choose(world.n_cities, 2) / 2)
    temperature = init_temperature

    old_distances = np.zeros(n_mc_samples)
    distances = np.zeros(n_mc_samples)
    swap_list = generate_swaplist(world.n_cities, neighbourhood)
    reverse_list = generate_reverselist(world.n_cities)
    np.random.shuffle(swap_list)

    print("==============")
    print("Starting simulated annealing with variables:")
    print(r"n_samples: {}, T_i: {}, f_c: {}, neighb.: {}".
          format(n_mc_samples,
                 init_temperature,
                 cooling_factor,
                 neighbourhood))
    print("==============")
    print("Temperature | Average sampled distance")
    new_sample_found = True
    epochs = 0
    border = 0.5  # probability of choosing the swap_cities() method
    while new_sample_found:
        new_sample_found = False
        swap_list_counter = 0
        reverse_list_counter = 0
        for sample_number in range(n_mc_samples):
            current_distance = world.tour.distance
            
            candidate_world = copy.deepcopy(world)

            if np.random.rand() < border:
                swap = swap_list[swap_list_counter]
                candidate_world.tour.swap_cities(swap)
                swap_list_counter += 1
            else:
                [from_city,to_city] = reverse_list[reverse_list_counter]
                candidate_world.tour.reverse_direction(from_city, to_city)
                reverse_list_counter += 1
                
            new_distance = candidate_world.tour.distance

            if accept(current_distance, new_distance, temperature):
                new_sample_found = True
                world = copy.deepcopy(candidate_world)
                
                np.random.shuffle(swap_list)
                np.random.shuffle(reverse_list)
                
                swap_list_counter = 0
                reverse_list_counter = 0
                border = 0.5
            else:
                # If all swaps or reverse directions are done, only the other
                # method is used in the future.
                if swap_list_counter == len(swap_list):
                    print("Tried all possible swap combinations.")
                    border = -1
                if reverse_list_counter == len(reverse_list):
                    print("Tried all possible reverse directions")
                    border = 2

            distances[sample_number] = world.tour.distance

        diff = old_distances.mean() - distances.mean()
        if diff > 0:
            trend = "\\/"
        elif diff == 0:
            trend = "--"
        else:
            trend = "/\\"
        print("    {0:3.3f}               {1:3.3f} {2}".format(temperature, distances[sample_number], trend))

        if show_steps:
            world.show()
            plt.pause(0.1)

        old_distances = copy.copy(distances)
        temperature *= cooling_factor
        n_mc_samples *= rising_mc_factor
#        tour_cities = [city.label for city in world.tour.tour]
#        print(tour_cities)
        epochs += 1

    return world


def choose(n, k):
    return np.math.factorial(n) / \
           (np.math.factorial(n - k) * np.math.factorial(k))


def p(tour: Tour, temperature: float):
    return np.exp(-tour.distance / temperature)


def generate_swaplist(n_cities: int, neighbourhood: int):
    index_list = [x for x in range(n_cities)]
    return list(combinations(index_list, neighbourhood))


def generate_reverselist(n_cities: int):
    reverselist = []
    from_city_log = []
    for from_city in range(n_cities):
        from_city_log.append(from_city)
        if from_city == n_cities-1:
            excl_city_front = 0
        else:
            excl_city_front = from_city + 1
        if from_city == 0:
            excl_city_back = n_cities-1
        else:
            excl_city_back = from_city - 1
        excl_list = [from_city, excl_city_front, excl_city_back]
        to_city_choices = [x for x in range(n_cities) if x not in excl_list if x not in from_city_log]
                
        for to_city in to_city_choices:
            reverselist.append([from_city,to_city])
    
    return reverselist


def accept(old_sample: float, candidate_sample: float, temperature: float):
    diff = candidate_sample - old_sample
    a = np.exp(- diff / temperature)

    if a >= 1:
        return True
    elif np.random.rand() <= a:
        return True
    else:
        return False
