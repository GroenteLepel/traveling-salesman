import copy
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt

from tour import Tour
from world import World


def sa_solution(world: World, n_mc_samples: int = -1, neighbourhood: int = 2,
                init_temperature: float = -1, cooling_factor: float = 0.9, rising_mc: bool = True,
                show_steps: bool = False):
    
    if rising_mc:
        rising_mc_factor = cooling_factor**-1
    else:
        rising_mc_factor = 1
        
    
    # Initialise the temperature
    if init_temperature < 0:
        init_temperature = world.n_cities / 8
    if n_mc_samples < 0:
        n_mc_samples = int(choose(world.n_cities, 2) / 2)
    temperature = init_temperature
    
    # Generate shuffled swap and reverse lists
    swap_list = generate_swaplist(world.n_cities, neighbourhood)
    reverse_list = generate_reverselist(world.n_cities)
    np.random.shuffle(swap_list)
    np.random.shuffle(reverse_list)
    
    # Calculate maximum amount of MC samples
    max_n_mc_samples = len(swap_list) + len(reverse_list)

    # Aesthetics
    print("==============")
    print("Starting simulated annealing with variables:")
    print(r"n_samples: {}, T_i: {}, f_c: {}, neighb.: {}".
          format(n_mc_samples,
                 init_temperature,
                 cooling_factor,
                 neighbourhood))
    print("==============")
    print("Temperature | # MC samples | Average epoch distance")
            
    new_sample_found = True
    epochs = 0
    border = 0.5  # probability of choosing the swap_cities() method
    epoch_average_distance = world.tour.distance
    while new_sample_found:
        new_sample_found = False
        
        # Go to the start of the lists since a new sample has just been found
        swap_list_counter = 0
        reverse_list_counter = 0
        
        # Save the average distance of the old epoch
        old_epoch_average_distance = epoch_average_distance
        
        sum_epoch_distances = 0
        for sample_number in range(n_mc_samples):
            current_distance = world.tour.distance  # save distance to compare with new trial state
            
            candidate_world = copy.deepcopy(world)

            # Choose between two methods for finding a new trial state
            if np.random.rand() < border:
                swap = swap_list[swap_list_counter]
                candidate_world.tour.swap_cities(swap)
                swap_list_counter += 1
            else:
                [from_city,to_city] = reverse_list[reverse_list_counter]
                candidate_world.tour.reverse_direction(from_city, to_city)
                reverse_list_counter += 1
                
            new_distance = candidate_world.tour.distance

            # Check whether to acccept the new state
            if accept(current_distance, new_distance, temperature):
                new_sample_found = True
                world = copy.deepcopy(candidate_world)
                
                # Shuffle the lists and start all over again since previously
                # skipped trials may now result in a lower energy.
                np.random.shuffle(swap_list)
                np.random.shuffle(reverse_list)
                swap_list_counter = 0
                reverse_list_counter = 0
                
                # Reset border
                border = 0.5
            else:
                # If all swaps or reverse directions are done, only the other
                # method is used in the future.
                if swap_list_counter == len(swap_list) and reverse_list_counter == len(reverse_list):
                    print("Tried all possible swaps and reverses.")
                    border = 0.5  # this does not matter since the loop will be stopped
                    
                elif swap_list_counter == len(swap_list):
                    if border != -1:
                        print("Tried all possible swap combinations.")
                        border = -1
                            
                elif reverse_list_counter == len(reverse_list):
                    if border != 2:
                        print("Tried all possible reverse directions.")
                        border = 2
                
            
            sum_epoch_distances += world.tour.distance

        epoch_average_distance = float(sum_epoch_distances) / n_mc_samples

        # Calculate the difference before and after the epoch
        diff_average = epoch_average_distance - old_epoch_average_distance
        if diff_average < 0:
            trend = "\\/"
        elif diff_average == 0:
            trend = "--"
        else:
            trend = "/\\"
        print("{0:3.3f}\t\t{1:d}\t\t{2:3.3f}  {3}".format(temperature, n_mc_samples, epoch_average_distance, trend))

        if show_steps:
            world.show()
            plt.pause(0.1)

        # Update temperature and the amount of MC samples
        temperature *= cooling_factor
        if temperature < 0.25:
            n_mc_samples = int(rising_mc_factor * n_mc_samples)
        if n_mc_samples > max_n_mc_samples:
            n_mc_samples = max_n_mc_samples
            temperature = 0
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
        excl_list = [from_city, excl_city_front, excl_city_back] + from_city_log
        to_city_choices = [x for x in range(n_cities) if x not in excl_list]
                
        for to_city in to_city_choices:
            reverselist.append([from_city,to_city])
    
    return reverselist


def accept(old_sample: float, candidate_sample: float, temperature: float):
    diff = candidate_sample - old_sample
    if temperature == 0:
        a = 0
    else:
        a = np.exp(- diff / temperature)

    if a >= 1:
        return True
    elif np.random.rand() <= a:
        return True
    else:
        return False
