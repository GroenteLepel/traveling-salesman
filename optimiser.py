import copy
import numpy as np
from itertools import combinations

from tour import Tour
from world import World


def optimise(world: World):
    sa_world = sa_solution(world)
    world = kruus_druut_hoalen(sa_world)
    return world


def sa_solution(world: World, n_mc_samples: int = -1, neighbourhood: int = 2,
                init_temperature: float = -1, cooling_factor: float = 0.9,
                show_steps: bool = False):
    if init_temperature < 0:
        init_temperature = world.n_cities / 8
    if n_mc_samples < 0:
        n_mc_samples = int(choose(world.n_cities, 2) / 2)
    temperature = init_temperature

    distances = np.zeros(n_mc_samples)
    swap_list = generate_swaplist(world.n_cities, neighbourhood)
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
    while new_sample_found:
        new_sample_found = False
        swap_list_counter = 0
        for _ in range(n_mc_samples):
            current_distance = world.tour.distance

            # swap = np.random.choice(world.n_cities, size=neighbourhood, replace=False)
            swap = swap_list[swap_list_counter]

            candidate_world = copy.deepcopy(world)
            candidate_world.tour.swap_cities(swap)
            new_distance = candidate_world.tour.distance

            if accept(current_distance, new_distance, temperature):
                new_sample_found = True
                world = copy.deepcopy(candidate_world)
                np.random.shuffle(swap_list)
                swap_list_counter = 0
            else:
                swap_list_counter += 1

                # if all the possibilities of the swap list have been checked,
                #  stop the monte carlo sampling. No new sample will be found.
                #  This can only happen if n_mc_samples > number of
                #  combinations.
                if swap_list_counter == len(swap_list):
                    print("Tried all possible combinations.")
                    break

            distances[_] = world.tour.distance
            diff = distances[_-1] - distances[_]
            if diff > 0:
                trend_str = "\/"
            else:
                trend_str = "/\\"
            print("    {0:3.3f}               {1:3.3f} {2}"
                  .format(temperature, distances[_], trend_str),
                  end='\r')

        if show_steps:
            world.show(
                r"$T$ = {0:.3f}, avg_dist = {1:.3f}".format(temperature,
                                                            distances.mean())
            )
        temperature *= cooling_factor

    return world


def kruus_druut_hoalen(world: World):
    pass


def choose(n, k):
    return np.math.factorial(n) / \
           (np.math.factorial(n - k) * np.math.factorial(k))


def p(tour: Tour, temperature: float):
    return np.exp(-tour.distance / temperature)


def generate_swaplist(n_cities: int, neighbourhood: int):
    index_list = [x for x in range(n_cities)]
    return list(combinations(index_list, neighbourhood))


def accept(old_sample: float, candidate_sample: float, temperature: float):
    diff = candidate_sample - old_sample
    a = np.exp(- diff / temperature)

    if a >= 1:
        return True
    elif np.random.rand() <= a:
        return True
    else:
        return False
