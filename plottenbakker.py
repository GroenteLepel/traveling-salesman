import matplotlib
import matplotlib.pyplot as plt
import pickle
import copy


def borderplot(borders, temp_lists, avg_dist_lists, stdev_dist_lists, title='border.png'):
    matplotlib.rcParams.update({'font.size': 18})
    minimal_distance = pickle.load(open("data/minimal_distance.p", "rb"))

    fig = plt.figure(constrained_layout=False, figsize=(10, 10))
    gs = fig.add_gridspec(nrows=len(temp_lists), ncols=2, wspace=0.25, hspace=0.1, left=0.15, right=0.9)

    axs = []

    temp_borders = [max(list(map(max, temp_lists))), min(list(map(min, temp_lists)))]
    avg_dist_borders = [5, max(list(map(max, avg_dist_lists)))]
    stdev_dist_borders = [-0.1, max(list(map(max, stdev_dist_lists)))]

    for i, border in enumerate(borders):
        axs.append([fig.add_subplot(gs[i, 0]), fig.add_subplot(gs[i, 1])])
        axs[i][0].set_ylabel('$P_{{swap}}$ = {0:4.2f}'.format(border))

        axs[i][0].plot(temp_lists[i], avg_dist_lists[i], color='black')
        axs[i][0].axhline(minimal_distance, xmin=temp_borders[0], xmax=temp_borders[1], linestyle='dashed', color='black')
        axs[i][0].set_xscale('log')
        axs[i][0].set_xlim(temp_borders[0], temp_borders[1])
        axs[i][0].set_ylim(avg_dist_borders[0], avg_dist_borders[1])
        if i == len(borders) - 1:
            axs[i][0].set_xticks([1e1, 1e0, 1e-1, 1e-2])
            axs[i][0].tick_params(axis='x', length=5, which='major')
        else:
            axs[i][0].set_xticks([1e1, 1e0, 1e-1, 1e-2])
            axs[i][0].tick_params(axis='x', length=5, which='major', labelsize=0)


        axs[i][1].plot(temp_lists[i], stdev_dist_lists[i], color='black')
        axs[i][1].axhline(0.0, xmin=temp_borders[0], xmax=temp_borders[1], linestyle='dashed', color='black')
        axs[i][1].set_xscale('log')
        axs[i][1].set_xlim(temp_borders[0], temp_borders[1])
        axs[i][1].set_ylim(stdev_dist_borders[0], stdev_dist_borders[1])
        axs[i][1].yaxis.tick_right()
        if i == len(borders) - 1:
            axs[i][1].set_xticks([1e1, 1e0, 1e-1, 1e-2])
            axs[i][1].tick_params(axis='x', length=5, which='major')
        else:
            axs[i][1].set_xticks([1e1, 1e0, 1e-1, 1e-2])
            axs[i][1].tick_params(axis='x', length=5, which='major', labelsize=0)

    fig.text(0.508, 0.91, 'Effect of the swap probability\non simulated annealing', ha='center')
    fig.text(0.508, 0.04, 'Temperature', ha='center')
    fig.text(0.02, 0.5, 'Average distance', va='center', rotation='vertical')
    fig.text(0.96, 0.5, '$\sigma$ distance', va='center', rotation='vertical')

    if title:
        fig.savefig('data/figures/{0:s}'.format(title))


def mc_sample_plot(n_mc_sample_list, temp_lists, avg_dist_lists, stdev_dist_lists, title='n_mc_sample.png'):
    matplotlib.rcParams.update({'font.size': 18})
    minimal_distance = pickle.load(open("data/minimal_distance.p", "rb"))

    fig = plt.figure(constrained_layout=False, figsize=(10, 10))
    gs = fig.add_gridspec(nrows=len(temp_lists), ncols=2, wspace=0.25, hspace=0.1, left=0.15, right=0.9)

    axs = []

    temp_borders = [max(list(map(max, temp_lists))), min(list(map(min, temp_lists)))]
    avg_dist_borders = [5, max(list(map(max, avg_dist_lists)))]
    stdev_dist_borders = [-0.1, max(list(map(max, stdev_dist_lists)))]

    for i, n_mc_samples in enumerate(n_mc_sample_list):
        axs.append([fig.add_subplot(gs[i, 0]), fig.add_subplot(gs[i, 1])])
        axs[i][0].set_ylabel('$n_{{MC}}$ = {}'.format(n_mc_samples))

        axs[i][0].plot(temp_lists[i], avg_dist_lists[i], color='black')
        axs[i][0].axhline(minimal_distance, xmin=temp_borders[0], xmax=temp_borders[1], linestyle='dashed', color='black')
        axs[i][0].set_xscale('log')
        axs[i][0].set_xlim(temp_borders[0], temp_borders[1])
        axs[i][0].set_ylim(avg_dist_borders[0], avg_dist_borders[1])
        if i == len(n_mc_sample_list) - 1:
            axs[i][0].set_xticks([1e1, 1e0, 1e-1, 1e-2])
            axs[i][0].tick_params(axis='x', length=5, which='major')
        else:
            axs[i][0].set_xticks([1e1, 1e0, 1e-1, 1e-2])
            axs[i][0].tick_params(axis='x', length=5, which='major', labelsize=0)


        axs[i][1].plot(temp_lists[i], stdev_dist_lists[i], color='black')
        axs[i][1].axhline(0.0, xmin=temp_borders[0], xmax=temp_borders[1], linestyle='dashed', color='black')
        axs[i][1].set_xscale('log')
        axs[i][1].set_xlim(temp_borders[0], temp_borders[1])
        axs[i][1].set_ylim(stdev_dist_borders[0], stdev_dist_borders[1])
        axs[i][1].yaxis.tick_right()
        if i == len(n_mc_sample_list) - 1:
            axs[i][1].set_xticks([1e1, 1e0, 1e-1, 1e-2])
            axs[i][1].tick_params(axis='x', length=5, which='major')
        else:
            axs[i][1].set_xticks([1e1, 1e0, 1e-1, 1e-2])
            axs[i][1].tick_params(axis='x', length=5, which='major', labelsize=0)

    fig.text(0.508, 0.91, 'Effect of the amount of mc samples\non simulated annealing', ha='center')
    fig.text(0.508, 0.04, 'Temperature', ha='center')
    fig.text(0.02, 0.5, 'Average distance', va='center', rotation='vertical')
    fig.text(0.96, 0.5, '$\sigma$ distance', va='center', rotation='vertical')

    if title:
        fig.savefig('data/figures/{0:s}'.format(title))
