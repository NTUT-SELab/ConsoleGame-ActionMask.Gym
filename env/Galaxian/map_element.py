import random as rnd

from env.Galaxian.map_define import *

class MapElement:
    def __init__(self, position, map):
        self.position = position
        self.status = True
        self.symbol = None
        self.map = map

    def get_position(self):
        return self.position

    def get_symbol(self):
        return self.symbol

    def move(self):
        pass

    def is_active(self):
        return self.status

    def disable(self):
        self.status = False

class Galaxian(MapElement):
    def __init__(self, position, map):
        super().__init__(position, map)
        self.symbol = MapEnum.galaxian.value

    def move(self, action):
        width = self.map.width
        #Left
        if action == 0 and self.position[1] > 1:
            self.position[1] -= 1
        # Right
        if action == 1 and self.position[1] < width - 2:
            self.position[1] += 1

    def fire(self):
        position = self.position.copy()
        return (Bullet(position, self.map))

class Enemy(MapElement):
    def __init__(self, position, map):
        super().__init__(position, map)
        self.approach_progress = 0
        self.symbol = MapEnum.enemy.value

    def move(self):
        if self.approach_progress < 6:
            self.approach_progress += 1
        else:
            self.approach_progress = 0
            self.position[0] += 1

class Bullet(MapElement):
    def __init__(self, position, map):
        super().__init__(position, map)
        self.symbol = MapEnum.bullet.value

    def move(self):
        self.position[0] -= 1
        if self.position[0] == 0:
            self.disable()
    
class Bonus(MapElement):
    def __init__(self, position, map):
        super().__init__(position, map)
        self.symbol = MapEnum.bonus.value
        self.direction = rnd.choice([-1, 1])
        self.activate_progress = 0
    
    def move(self):
        if not self.status:
            return

        self.change_direction()

        if self.direction == -1:
            self.position[1] -= 1
        else:
            self.position[1] += 1


    def change_direction(self): 
        left_end = 1
        right_end = self.map.width - 2

        # AT THE LEFT END
        if self.position[1] == left_end:
            self.direction = 1
        # AT THE RIGHT END
        if self.position[1] == right_end:
            self.direction = -1

    def reactivate(self):
        if not self.status:
            self.position[1] = rnd.randint(1, self.map.width - 2)
            self.status = True

