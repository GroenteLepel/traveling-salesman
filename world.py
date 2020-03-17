import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from city import City
from tour import Tour
from rcarry.generator import rcarry


class World:
    def __init__(self, n_cities: int):
        self.n_cities = n_cities
        self.cities = self._gen_cities()
        self.tour = Tour(self.cities)

    def _gen_cities(self):
        return [City(rcarry.generate(), rcarry.generate(), _) for _ in
                range(self.n_cities)]

    def show(self, title=None):
        plt.clf()
        for city in self.cities:
            plt.scatter(city.x, city.y, label="City {}".format(city.label))

        for i in range(self.n_cities):
            from_city = self.tour.tour[i]
            if i + 1 == self.n_cities:
                to_city = self.tour.tour[0]
            else:
                to_city = self.tour.tour[i+1]
            plt.plot([from_city.x, to_city.x], [from_city.y, to_city.y])

        #plt.legend()
        if title:
            plt.savefig('data/figures/{0:s}.jpg'.format(title))
        plt.show()
    
    def show_withplots(self, temperature_list, avg_distance_list, stdev_distance_list, title=None):
        matplotlib.rcParams.update({'font.size': 18})

        fig = plt.figure(constrained_layout=False, figsize=(8, 12))
        gs = fig.add_gridspec(nrows=3, ncols=2, wspace=0.1, hspace=0.1)

        world_ax = fig.add_subplot(gs[0:-1, :])
        avgdist_ax = fig.add_subplot(gs[2, 0])
        stdevdist_ax = fig.add_subplot(gs[2, 1])

        for city in self.cities:
            world_ax.scatter(city.x, city.y, label="City {}".format(city.label))

        for i in range(self.n_cities):
            from_city = self.tour.tour[i]
            if i + 1 == self.n_cities:
                to_city = self.tour.tour[0]
            else:
                to_city = self.tour.tour[i+1]
            world_ax.plot([from_city.x, to_city.x], [from_city.y, to_city.y], color='black')
        world_ax.set_xticklabels([])
        world_ax.set_yticklabels([])
        world_ax.xaxis.set_visible(False)
        world_ax.yaxis.set_visible(False)


        temperature_list.reverse()

        avgdist_ax.plot(temperature_list, avg_distance_list, color='black')
        # avgdist_ax.set_title('$AVG_{dist}$ vs temperature')
        avgdist_ax.set_xscale('log')
        avgdist_ax.set_xlabel('Temperature')
        avgdist_ax.set_ylabel('Average distance')


        stdevdist_ax.plot(temperature_list, stdev_distance_list, color='black')
        # stdevdist_ax.set_title('$\sigma_{dist}$ vs temperature')
        stdevdist_ax.set_xscale('log')
        stdevdist_ax.set_xlabel('Temperature')
        stdevdist_ax.set_ylabel('$\sigma$ distance')
        stdevdist_ax.yaxis.set_label_position("right")
        stdevdist_ax.yaxis.tick_right()

        if title:
            fig.savefig('data/figures/{0:s}'.format(title))

        fig.show()