from world import World
import optimiser
import plottenbakker as pb
import numpy as np
import time
import pickle

minimal_distance = pickle.load(open("data/minimal_distance.p", "rb"))

# my_world = pickle.load(open("data/init_world.p", "rb"))
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


# %% border plot
# borders = [0.1, 0.5, 0.9]
# temp_lists, avg_dist_lists, stdev_dist_lists = [], [], []
# for border in borders:
#     my_world = pickle.load(open("data/init_world.p", "rb"))
#     optimised_world, final_distance, [temperature_list, avg_distance_list, stdev_distance_list] = \
#         optimiser.sa_solution(world=my_world,
#                               n_mc_samples=300,
#                               neighbourhood=2,
#                               init_temperature=10.0,
#                               cooling_factor=0.95,
#                               init_swap_probability=border,
#                               rising_mc=False,
#                               show_steps=False,
#                               title=None)
#     temp_lists.append(temperature_list)
#     avg_dist_lists.append(avg_distance_list)
#     stdev_dist_lists.append(stdev_distance_list)
#
# pb.borderplot(borders, temp_lists, avg_dist_lists, stdev_dist_lists, title='paramtest_p_swap.png')
# for avg_dist_list in avg_dist_lists:
#     print(avg_dist_list[-1]/minimal_distance)


#%% average the final distance over 10 runs for the borders given above
# minimal_distance = pickle.load(open("data/minimal_distance.p", "rb"))
# borders = [0.1, 0.5, 0.9]
# runs = 10
#
# run_times = np.zeros(len(borders), dtype=float)
# final_distances = np.array([[0]*runs]*len(borders), dtype=float)
# for run in range(runs):
#     for border_index, border in enumerate(borders):
#         print("\nRun {} - border {}".format(run, border))
#         my_world = pickle.load(open("data/init_world.p", "rb"))
#         start_time = time.time()
#         _, final_distance, _ = \
#             optimiser.sa_solution(world=my_world,
#                                   n_mc_samples=300,
#                                   neighbourhood=2,
#                                   init_temperature=10.0,
#                                   cooling_factor=0.95,
#                                   init_swap_probability=border,
#                                   rising_mc=False,
#                                   show_steps=False,
#                                   title=None)
#         run_time = time.time() - start_time
#         run_times[border_index] += run_time
#         final_distances[border_index][run] += final_distance
#
# run_times = np.array(np.round(run_times/runs), dtype=int)
# final_distances /= minimal_distance
# pickle.dump(final_distances, open("data/final_distances_10runs.p", "wb"))
#
# avg_fin_dists, stdev_fin_dists = np.zeros(len(borders), dtype=float), np.zeros(len(borders), dtype=float)
# for border_index in range(len(borders)):
#     avg_fin_dists[border_index] = np.average(final_distances[border_index])
#     stdev_fin_dists[border_index] = np.std(final_distances[border_index])
#
# for border_index, border in enumerate(borders):
#     print("\n\nAverage results over {} runs:".format(runs))
#     print("P_swap\tAverage final distance\tStdev final distance\tRuntime in seconds")
#     print("{0:.2f}\t\t{1:.3f}\t\t{2:.3f}\t\t{3:d}".format(border,
#                                                          avg_fin_dists[border_index],
#                                                          stdev_fin_dists[border_index],
#                                                          run_times[border_index]))

#%%
# psawp = 0.1
# minimal_distance = pickle.load(open("data/minimal_distance.p", "rb"))
# while True:
#     my_world = pickle.load(open("data/init_world.p", "rb"))
#     optimised_world, final_distance, _ = \
#         optimiser.sa_solution(world=my_world,
#                               n_mc_samples=300,
#                               neighbourhood=2,
#                               init_temperature=10.0,
#                               cooling_factor=0.95,
#                               init_swap_probability=psawp,
#                               rising_mc=True,
#                               show_steps=False,
#                               title=None)
#     print("\nFinal distance = {0:.6f}".format(final_distance))
#     print("Minimal distance = {0:.6f}".format(minimal_distance))
#     if final_distance < minimal_distance:
#         minimal_distance = final_distance
#         pickle.dump(minimal_distance, open("data/minimal_distance.p", "wb"))
#         pickle.dump(optimised_world, open("data/best_world.p", "wb"))


#%% n mc samples
n_mc_sample_list = [100, 'dynamic', 1000]
temp_lists, avg_dist_lists, stdev_dist_lists = [], [], []
for n_mc_samples in n_mc_sample_list:
    rising_mc = False
    if n_mc_samples == 'dynamic':
        n_mc_samples = 300
        rising_mc = True
    my_world = pickle.load(open("data/init_world.p", "rb"))
    optimised_world, final_distance, [temperature_list, avg_distance_list, stdev_distance_list] = \
        optimiser.sa_solution(world=my_world,
                              n_mc_samples=n_mc_samples,
                              neighbourhood=2,
                              init_temperature=10.0,
                              cooling_factor=0.95,
                              init_swap_probability=0.1,
                              rising_mc=rising_mc,
                              show_steps=False,
                              title=None)
    temp_lists.append(temperature_list)
    avg_dist_lists.append(avg_distance_list)
    stdev_dist_lists.append(stdev_distance_list)

pb.mc_sample_plot(n_mc_sample_list, temp_lists, avg_dist_lists, stdev_dist_lists, title='paramtest_n_mc_samples_pswap0.1.png')
for avg_dist_list in avg_dist_lists:
    print(avg_dist_list[-1]/minimal_distance)


#%% 10 runs n mc samples
minimal_distance = pickle.load(open("data/minimal_distance.p", "rb"))
n_mc_sample_list = [100, 'dynamic', 1000]
runs = 10

run_times = np.zeros(len(n_mc_sample_list), dtype=float)
final_distances = np.array([[0]*runs]*len(n_mc_sample_list), dtype=float)
for run in range(runs):
    for n_mc_samples_index, n_mc_samples in enumerate(n_mc_sample_list):
        rising_mc = False
        print("\nRun {} - n mc samples {}".format(run, n_mc_samples))
        if n_mc_samples == 'dynamic':
            n_mc_samples = 300
            rising_mc = True
        my_world = pickle.load(open("data/init_world.p", "rb"))
        start_time = time.time()
        _, final_distance, _ = \
            optimiser.sa_solution(world=my_world,
                              n_mc_samples=n_mc_samples,
                              neighbourhood=2,
                              init_temperature=10.0,
                              cooling_factor=0.95,
                              init_swap_probability=0.5,
                              rising_mc=rising_mc,
                              show_steps=False,
                              title=None)
        run_time = time.time() - start_time
        run_times[n_mc_samples_index] += run_time
        final_distances[n_mc_samples_index][run] += final_distance

run_times = np.array(np.round(run_times/runs), dtype=int)
final_distances /= minimal_distance
pickle.dump(final_distances, open("data/final_distances_10runs_n_mc_changes.p", "wb"))

avg_fin_dists, stdev_fin_dists = np.zeros(len(n_mc_sample_list), dtype=float), np.zeros(len(n_mc_sample_list), dtype=float)
for n_mc_samples_index in range(len(n_mc_sample_list)):
    avg_fin_dists[n_mc_samples_index] = np.average(final_distances[n_mc_samples_index])
    stdev_fin_dists[n_mc_samples_index] = np.std(final_distances[n_mc_samples_index])

for n_mc_samples_index, n_mc_samples in enumerate(n_mc_sample_list):
    print("\n\nAverage results over {} runs:".format(runs))
    print("n mc samples\tAverage final distance\tStdev final distance\tRuntime in seconds")
    print("{0}\t\t{1:.3f}\t\t{2:.3f}\t\t{3:d}".format(n_mc_samples,
                                                         avg_fin_dists[n_mc_samples_index],
                                                         stdev_fin_dists[n_mc_samples_index],
                                                         run_times[n_mc_samples_index]))

#%%
init_world = pickle.load(open("data/init_world.p", "rb"))
init_world.show('init_world.png')
best_world = pickle.load(open('data/best_world.p', 'rb'))
best_world.show('best_world.png')