import numpy as np

from city import City
from typing import List
import copy


class Tour:
    def __init__(self, cities: List[City]):
        self.tour = copy.deepcopy(cities)
        self.distance = self.get_distance()

    def get_distance(self):
        distance = 0
        for i in range(len(self.tour)):
            from_city = self.tour[i]
            if i + 1 == len(self.tour):
                destination_city = self.tour[0]
            else:
                destination_city = self.tour[i + 1]

            distance += from_city.distance_to(destination_city)

        return distance

    def calculate_connection_distance(self, at_index: int):
        if at_index == len(self.tour) - 1:
            return self.tour[at_index].distance_to(self.tour[at_index - 1]) + \
                   self.tour[at_index].distance_to(self.tour[0])
        else:
            return self.tour[at_index].distance_to(self.tour[at_index - 1]) + \
                   self.tour[at_index].distance_to(self.tour[at_index + 1])

    def reverse_direction(self, from_city: int, to_city: int):
        """
        Reverse the direction in the tour from element from_city to element
        to_city.
        """
        if to_city >= len(self.tour):
            raise Exception("index out of bounds for list of length",
                            len(self.tour))
        elif to_city == from_city or to_city - from_city == 1:
            raise Exception("Slice size of zero or one is non-reversable.")

        if to_city < from_city:
            double_tour = self.tour + self.tour
            slice_to_reverse = double_tour[from_city:len(self.tour) + to_city]
            double_tour[from_city:len(self.tour) + to_city] = \
                slice_to_reverse.reverse()
            new_tour = double_tour[from_city:len(self.tour) + from_city]
            self.tour = new_tour
        else:
            slice_to_reverse = self.tour[from_city:to_city]
            self.tour[from_city:to_city] = slice_to_reverse.reverse()
        pass

    def swap_cities(self, to_swap: List[int]):
        cities = [City] * len(to_swap)
        to_reduce, to_add = 0, 0
        for _, swap_index in enumerate(to_swap):
            cities[_] = self.tour[swap_index]
            to_reduce += self.calculate_connection_distance(swap_index)

        back_city = cities[-1]
        cities.pop()
        cities.insert(0, back_city)

        for _, swap_index in enumerate(to_swap):
            self.tour[swap_index] = cities[_]

        for swap_index in to_swap:
            to_add += self.calculate_connection_distance(swap_index)

        self.distance += to_add - to_reduce
