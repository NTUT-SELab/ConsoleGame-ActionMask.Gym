import numpy as np
from env.Galaxian.map_define import *

class Map:
    def __init__(self, high, width):
        self.high = high
        self.width = width
        self.data = None
        self.map_elements = []

    def generate_data(self):
        self.data = np.full((self.high, self.width), MapEnum.space.value)
        self.data[0] = MapEnum.wall.value
        self.data[self.high - 1] = MapEnum.wall.value
        self.data[:, 0] = MapEnum.wall.value
        self.data[:, self.width - 1] = MapEnum.wall.value

    def add_element(self, element):
        self.map_elements.append(element)

    def add_elements(self, elements):
        self.map_elements += elements

    def clear_elements(self):
        del self.map_elements
        self.map_elements = []

    def refresh(self):
        self.generate_data()
        for element in self.map_elements:
            if element.is_active():
                position = element.get_position()
                self.data[position[0]][position[1]] = element.get_symbol()

