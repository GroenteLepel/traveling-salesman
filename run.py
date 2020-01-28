from world import World
from optimiser import optimise

n_mc_samples = 50000
init_temperature = 0.1
cooling_factor = 0.8

my_world = World(10)
optimised_world = optimise(my_world, n_mc_samples, init_temperature, cooling_factor)
optimised_world.show()