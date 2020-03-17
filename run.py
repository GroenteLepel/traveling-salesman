from world import World
import optimiser

my_world = World(50)
optimised_world, final_distance, [temperature_list, avg_distance_list, stdev_distance_list] = \
    optimiser.sa_solution(world=my_world,
                          n_mc_samples=300,
                          neighbourhood=2,
                          init_temperature=0.1,
                          cooling_factor=0.95,
                          init_swap_probability=1.0,
                          rising_mc=False,
                          show_steps=False,
                          title='swap_solution.png')

# %%
# optimised_world.show_withplots(temperature_list, avg_distance_list, stdev_distance_list)