import random as rnd
import numpy as np
import string
from env.MagicKey.map_define import *

class TextElement:
    def __init__(self, position, size):
        self.position = position
        self.status = True
        self.size = size
        self.left_reward = 0

    def move(self, steps):
        self.position[0] += steps

    def is_game_end(self):
        return False
    
    def get_weapon(self):
        return None

    def disable(self):
        self.status = False

class TextBallon(TextElement):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.texts = np.random.choice(list(string.ascii_uppercase), size=size)[0]
        self.to_graph()
        self.reward = 0
        self.left_reward = self.size[1]*self.size[2]

    def remove(self, key):
        self.reward = len(self.texts[self.texts == key])
        self.left_reward  = self.left_reward - self.reward
        self.texts[self.texts == key] = ' '
        if len(self.texts[self.texts != ' ']) == 0:
            self.disable()
        self.to_graph()

    def eliminate_by_weapon(self):
        self.disable()
        self.reward = self.left_reward

    def is_game_end(self):
        return True

    def to_graph(self):
        self.graph = np.insert(self.texts, 0, np.full((1, 1), '|'), 1)
        self.graph = np.insert(self.graph, self.graph.shape[1], np.full((1, 1), '|'), 1)
        self.graph =  np.insert(self.graph, 0, np.full((1, self.graph.shape[1]), '-'), 0)
        self.graph =  np.insert(self.graph, self.graph.shape[0], np.full((1, self.graph.shape[1]), '-'), 0)
        

class TextBonus(TextElement):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.quantity = np.random.randint(1, 10)
        self.texts = list(np.random.choice(list(string.ascii_uppercase), self.quantity))
        self.to_graph()
        self.reward = 0

    def remove(self, key):
        if len(self.texts) > 0 and self.texts[0] == key:
            del self.texts[0]
     
        if len(self.texts) == 0:
            self.disable()
            self.reward = self.quantity * 2
        else:
            self.to_graph()

    def to_graph(self):
        self.graph = np.full((1, 3), MapEnum.bonus_edge.value)
        self.graph[0,1] = self.texts[0]
        
class TextWeapon(TextElement):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.quantity = np.random.randint(1, 10)
        self.texts = list(np.random.choice(list(string.ascii_uppercase), self.quantity))
        self.to_graph()
        self.reward = 0

    def remove(self, key):
        if len(self.texts) > 0 and self.texts[0] == key:
            del self.texts[0]
     
        if len(self.texts) == 0:
            self.disable()
        else:
            self.to_graph()

    def get_weapon(self):
        if len(self.texts) == 0:
            return Weapon(int(self.quantity*0.5) + 1)
        else:
            return None

    def to_graph(self):
        self.graph = np.full((1, 3), MapEnum.weapon_edge.value)
        self.graph[0,1] = self.texts[0]

class Wizard:
    def __init__(self, position):
        self.position = position
        self.weapons = []
        self.key = ' '

    def receive_weapon(self, weapon):
        if weapon != None:
            if len(self.weapons) < 6:
                self.weapons.append(weapon)
            else:
                self.weapons[0] = weapon

    def use_weapon(self):
        power = 0
        if len(self.weapons) > 0:
            power = self.weapons[0].power
            del self.weapons[0]
        return power

    def shoot(self, action):
        if action < 26:
            key = chr(action+65)
        elif action == 26:
            key = '*'
        self.key = key

class Weapon:
    def __init__(self, power):
        self.power = power

