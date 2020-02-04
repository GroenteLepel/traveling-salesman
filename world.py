import numpy as np
import matplotlib.pyplot as plt

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

    def show(self):
        plt.clf()
        for n, city in enumerate(self.cities):
            plt.scatter(city.x, city.y, label="City {}".format(n))

        for i in range(self.n_cities):
            from_city = self.tour.tour[i]
            if i + 1 == self.n_cities:
                to_city = self.tour.tour[0]
            else:
                to_city = self.tour.tour[i+1]
            plt.plot([from_city.x, to_city.x], [from_city.y, to_city.y], c='b')

        #plt.legend()
        plt.show()