import numpy as np
from env.MagicKey.map_define import *
from env.MagicKey.map_element import Wizard

class Map:
    def __init__(self, high, width):
        self.high = high
        self.width = width
        self.data = None
        self.elements = []
        self.wizard = Wizard([high -2, int(width / 2)])
        self.generate_data()
        
    def generate_data(self):
        self.data = np.full((self.high, self.width), MapEnum.space.value)
        self.data[0] = MapEnum.wall.value
        self.data[self.high - 1] = MapEnum.wall.value
        self.data[:, 0] = MapEnum.wall.value
        self.data[:, self.width - 1] = MapEnum.wall.value
        self.data[self.high-3,1:self.width-1] = MapEnum.line_of_defense.value
        self.data[self.wizard.position[0], self.wizard.position[1]] = MapEnum.wizard.value

    def add_element(self, element):
        self.elements.append(element)

    def add_elements(self, elements):
        self.elements += elements
        
    def remove_elements(self):
        weapons = []
        while any([element.status == False for element in self.elements]):
            for element in self.elements:
                if not element.status:
                    self.wizard.receive_weapon(element.get_weapon())

                if element.position[0] + element.graph.shape[0] >= self.high - 3:
                    element.disable()

                if not element.status:
                    self.elements.remove(element)

    def eliminate_texts_by_weapon(self):
        power = self.wizard.use_weapon()
        for i in range(len(self.elements)):
            if power == 0:
                break
            if self.elements[i].status and self.elements[i].is_game_end():
                self.elements[i].eliminate_by_weapon()
                power -= 1
            
    def is_end(self):
        for element in self.elements:
            if element.position[0]+element.graph.shape[0] >= self.high - 3 and element.status:
                if element.is_game_end():
                    element.disable()
                    return True
                else:
                    element.disable()
        return False

    def refresh(self):
        del self.data
        self.generate_data()
        self.remove_elements()
        self.data[self.wizard.position[0] - 1, self.wizard.position[1]] = self.wizard.key

        for element in self.elements:
            start_x = element.position[1]
            start_y = element.position[0]
            high = start_y + element.graph.shape[0]
            width = start_x + element.graph.shape[1]
            self.data[start_y:high, start_x:width] = element.graph
        
        for weapon in self.wizard.weapons:
            i = self.wizard.weapons.index(weapon)
            self.data[self.high-2, i+1] = weapon.power