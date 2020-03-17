from world import World
import optimiser
import plottenbakker as pb

# my_world = World(50)
# optimised_world, final_distance, [temperature_list, avg_distance_list, stdev_distance_list] = \
#     optimiser.sa_solution(world=my_world,
#                           n_mc_samples=300,
#                           neighbourhood=2,
#                           init_temperature=10.0,
#                           cooling_factor=0.95,
#                           init_swap_probability=1.0,
#                           rising_mc=False,
#                           show_steps=False,
#                           title='plotje.png')

# %%
borders = [0.1, 0.5, 0.9]
temp_lists, avg_dist_lists, stdev_dist_lists = [], [], []
for border in borders:
    my_world = World(50)
    optimised_world, final_distance, [temperature_list, avg_distance_list, stdev_distance_list] = \
        optimiser.sa_solution(world=my_world,
                              n_mc_samples=300,
                              neighbourhood=2,
                              init_temperature=10.0,
                              cooling_factor=0.95,
                              init_swap_probability=border,
                              rising_mc=False,
                              show_steps=False,
                              title=None)
    temp_lists.append(temperature_list)
    avg_dist_lists.append(avg_distance_list)
    stdev_dist_lists.append(stdev_distance_list)

#%%
pb.borderplot(borders, temp_lists, avg_dist_lists, stdev_dist_lists, title='paramtest_p_swap.png')