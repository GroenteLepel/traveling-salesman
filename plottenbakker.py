import matplotlib
import matplotlib.pyplot as plt
import pickle


minimal_distance = pickle.load(open("data/minimal_distance.p", "rb"))


def borderplot(borders, temp_lists, avg_dist_lists, stdev_dist_lists, title='border.png'):
    matplotlib.rcParams.update({'font.size': 18})

    fig = plt.figure(constrained_layout=False, figsize=(8, 12))
    gs = fig.add_gridspec(nrows=len(temp_lists), ncols=2, wspace=0.2, hspace=0.1)

    axs = []

    temp_borders = [max(list(map(max, temp_lists))), min(list(map(min, temp_lists)))]
    avg_dist_borders = [5, max(list(map(max, avg_dist_lists)))]
    stdev_dist_borders = [-0.1, max(list(map(max, stdev_dist_lists)))]

    for i, border in enumerate(borders):
        axs.append([fig.add_subplot(gs[i, 0]), fig.add_subplot(gs[i, 1])])
        axs[i][0].set_ylabel('$P_{{swap}}$ = {0:4.2f}'.format(border))

        axs[i][0].plot(temp_lists[i], avg_dist_lists[i], color='black')
        axs[i][0].plot(temp_borders, [minimal_distance] * 2, linestyle='dashed', color='black')
        axs[i][0].set_xscale('log')
        axs[i][0].set_xlim(temp_borders[0], temp_borders[1])
        axs[i][0].set_ylim(avg_dist_borders[0], avg_dist_borders[1])
        if i == len(borders) - 1:
            axs[i][0].set_xticks([1e1, 1e0, 1e-1, 1e-2])
        else:
            axs[i][0].set_xticks([])


        axs[i][1].plot(temp_lists[i], stdev_dist_lists[i], color='black')
        axs[i][1].plot(temp_borders, [0.0] * 2, linestyle='dashed', color='black')
        axs[i][1].set_xscale('log')
        axs[i][1].set_xlim(temp_borders[0], temp_borders[1])
        axs[i][1].set_ylim(stdev_dist_borders[0], stdev_dist_borders[1])
        axs[i][1].yaxis.tick_right()
        if i == len(borders) - 1:
            axs[i][1].set_xticks([1e1, 1e0, 1e-1, 1e-2])
        else:
            axs[i][1].set_xticks([])

    fig.text(0.5, 0.04, 'Temperature', ha='center')
    fig.text(0.04, 0.5, 'Average distance', va='center', rotation='vertical')
    fig.text(1.04, 0.5, '$\sigma$ distance', va='center', rotation='vertical')

    if title:
        fig.savefig('data/figures/{0:s}'.format(title))
