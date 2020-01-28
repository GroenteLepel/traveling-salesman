from city import City
from typing import List


class Tour:
    def __init__(self, cities: List[City]):
        self.tour = cities
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

    def swap_cities(self, i: int, j: int):
        city1 = self.tour[i]
        city2 = self.tour[j]
        
        self.tour[i] = city2
        self.tour[j] = city1