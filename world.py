import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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
        if title != None:
            plt.savefig('../figures/{0:s}.png'.format(title))
        plt.show()
    
    def show_withplots(self, temperature_list, avg_distance_list, stdev_distance_list):
        fig = plt.figure(figsize=(8, 12))
        outer = gridspec.GridSpec(2, 1, wspace=0.2, hspace=0.2)
        
        world_ax = plt.Subplot(fig, outer[0,0])
        for city in self.cities:
            world_ax.scatter(city.x, city.y, label="City {}".format(city.label))

        for i in range(self.n_cities):
            from_city = self.tour.tour[i]
            if i + 1 == self.n_cities:
                to_city = self.tour.tour[0]
            else:
                to_city = self.tour.tour[i+1]
            world_ax.plot([from_city.x, to_city.x], [from_city.y, to_city.y])
        fig.add_subplot(world_ax)
        
        inner = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=outer[1,0], wspace=0.2, hspace=0.3)
        
        ax0 = plt.Subplot(fig, inner[0], xscale='log', title='$AVG_{dist}$ vs temperature')
        ax0.plot(temperature_list, avg_distance_list)
        fig.add_subplot(ax0)
        
        ax1 = plt.Subplot(fig, inner[1], xscale='log', title='$\sigma_{dist}$ vs temperature')
        ax1.plot(temperature_list, stdev_distance_list)
        fig.add_subplot(ax1)
        
        plt.style.use('grayscale')
        fig.savefig('test.png')