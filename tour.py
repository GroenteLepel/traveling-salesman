import numpy as np

from city import City
from typing import List
import copy


class Tour:
    def __init__(self, cities: List[City]):
        self.tour = copy.deepcopy(cities)
        self.distance_matrix = self._gen_distance_matrix()
        self.distance = self.get_distance()

    def _gen_distance_matrix(self):
        """
        Generates a symmetric matrix containing the distance between city i and
        city j at index [i][j], diagonal is zero.
        """
        n = len(self.tour)
        matrix = np.zeros(shape=(n, n))
        for i in range(n):
            for j in range(i):
                distance = self.tour[i].distance_to(self.tour[j])
                matrix[i][j], matrix[j][i] = distance, distance
        return matrix

    def get_distance(self):
        n = len(self.tour)
        distance = 0
        for i in range(n):
            from_city = self.tour[i].label
            if i + 1 == n:
                to_city = self.tour[0].label
            else:
                to_city = self.tour[i + 1].label

            distance += self.distance_matrix[from_city][to_city]

        return distance

    def calculate_connection_distance(self, at_index: int):
        # Should be useless now we have distance matrix.
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
            slice_to_reverse.reverse()
            double_tour[from_city:len(self.tour) + to_city] = \
                slice_to_reverse
            new_tour = double_tour[from_city:len(self.tour) + from_city]
            self.tour = new_tour
        else:
            slice_to_reverse = self.tour[from_city:to_city]
            slice_to_reverse.reverse()
            self.tour[from_city:to_city] = slice_to_reverse

    def swap_cities(self, to_swap: List[int]):
        # list of cities which are going to swap
        cities_to_swap = [City] * len(to_swap)
        # # values to add and reduce from total distance
        # to_reduce, to_add = 0, 0
        for i, swap_index in enumerate(to_swap):
            cities_to_swap[i] = self.tour[swap_index]
            # to_reduce += self.calculate_connection_distance(swap_index)

        # shift all the cities down one spot as a swap action.
        back_city = cities_to_swap[-1]
        cities_to_swap.pop()
        cities_to_swap.insert(0, back_city)

        for i, swap_index in enumerate(to_swap):
            self.tour[swap_index] = cities_to_swap[i]

        # for swap_index in to_swap:
        #     to_add += self.calculate_connection_distance(swap_index)

        self.distance = self.get_distance()
