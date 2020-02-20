from world import World
import optimiser

my_world = World(60)
optimised_world = optimiser.sa_solution(world = my_world,  
                                        n_mc_samples = 100, 
                                        neighbourhood = 2,
                                        init_temperature = -1, 
                                        cooling_factor = 0.9,
                                        rising_mc_factor = 1,
                                        show_steps = True)
optimised_world.show(title = '1')