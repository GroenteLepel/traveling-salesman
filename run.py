from world import World
import optimiser

my_world = World(50)
optimised_world = optimiser.sa_solution(world = my_world,  
                                        n_mc_samples = 300,
                                        neighbourhood = 2,
                                        init_temperature = 1.0,
                                        cooling_factor = 0.92,
                                        rising_mc = False,
                                        show_steps = False,
                                        title = 'plotje.jpg')