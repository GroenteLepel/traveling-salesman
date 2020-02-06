from world import World
import optimiser

my_world = World(30)
optimised_world = optimiser.sa_solution(world = my_world,  
                                        n_mc_samples = 100, 
                                        neighbourhood = 2,
                                        init_temperature = -1, 
                                        cooling_factor = 0.9,
                                        show_steps = False)
optimised_world.show(title = '1')