import numpy as np


class City:
    def __init__(self, x: float, y: float, label: int):
        self.x = x
        self.y = y
        self.label = label

    def distance_to(self, destination_city):
        dx = np.abs(self.x - destination_city.x)
        dy = np.abs(self.y - destination_city.y)

        return np.sqrt(dx ** 2 + dy ** 2)
