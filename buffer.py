from typing import List
from pprint import pprint


class Unit:
    def __init__(self, x, y=0):
        self.x = x
        self.y = y

    def get_coords(self):
        return self.x, self.y


class Zombie(Unit):
    def __init__(self, move_index, row, hp):
        super().__init__(row)
        self.move_index = move_index
        self.hp = hp

    def __repr__(self):
        return f"Zombie {self.hp} hp on ({self.x},{self.y}) position"

    def move_zombie(self):
        self.y -= 1


class Shooter(Unit):
    def __init__(self, x: int, y: int, power: int = 1):
        super().__init__(x, y)
        self.power = power

    def __repr__(self):
        return f"Plant at ({self.x}, {self.y}) coord"

    def __str__(self):
        return f"{self.power}"

    def shooting(self, zombie_list: List[Zombie]):
        current_shots = self.power
        # returns list of zombies that can be damaged, they are sorted by y coord
        zombies_under_fire = sorted(list(filter(lambda zombie: self.x == zombie.x, zombie_list)),
                                    key=lambda zombie: zombie.y)

        for zombie in zombies_under_fire:
            if current_shots <= 0:
                break

            zombie.hp, current_shots = zombie.hp - current_shots, current_shots - zombie.hp
            if zombie.hp <= 0:
                zombie_list.remove(zombie)


class SShooter(Shooter):
    def __init__(self, x, y):
        super().__init__(x, y)

    def __str__(self):
        return "S"

    def calculate_range(self, field):
        row_len = len(field[0])
        column_len = len(field)

        # performs horizontal and diagonal range under fire
        range_list = [(self.x, y) for y in range(self.y, row_len)]
        for y, x in enumerate(range(self.x, column_len), self.y):
            range_list.append((x, y))
        for y, x in enumerate(range(self.x, -1, -1), self.y):
            range_list.append((x, y))
        return range_list

    def s_shooting(self, zombie_list: List[Zombie], field: list):
        zombies_under_fire = []
        zombies_under_range = list(filter(lambda zombie: zombie.get_coords() in self.calculate_range(field),
                                          zombie_list))
        up_r_zombies = sorted(list(filter(lambda zombie: zombie.get_coords()[0] > self.x, zombies_under_range)),
                              key=lambda zombie: zombie.y)
        down_r_zombies = sorted(list(filter(lambda zombie: zombie.get_coords()[0] < self.x, zombies_under_range)),
                                key=lambda zombie: zombie.y)
        middle_zombies = sorted(list(filter(lambda zombie: zombie.get_coords()[0] == self.x, zombies_under_range)),
                                key=lambda zombie: zombie.y)
        for l in (up_r_zombies, down_r_zombies, middle_zombies):
            if l:
                zombies_under_fire.append(l[0])
        for zombie in zombies_under_fire:
            zombie.hp -= 1
            if zombie.hp == 0:
                zombie_list.remove(zombie)


class BattleField:
    def __init__(self, field: list, zombies: list):
        self._field = field
        self._zombies = [Zombie(*i) for i in zombies]
        self._move_index = 0
        self.shooters_list: List[Shooter] = []
        self.s_shooters_list: List[SShooter] = []
        self._zombies_in_battle: List[Zombie] = []
        self.set_shooters()

    def set_shooters(self):
        """spawning the plants"""
        for i in range(len(self._field)):
            for j in range(len(self._field[i])):
                if self._field[i][j].isdigit():
                    self.shooters_list.append(Shooter(i, j, int(self._field[i][j])))
                elif self._field[i][j] == "S":
                    self.s_shooters_list.append(SShooter(i, j))
        self.s_shooters_list.sort(key=(lambda plant: (plant.y, -plant.x)), reverse=True)

    def set_zombies(self):
        """this method is spawning zombies"""
        zombies_to_remove = []
        for zombie in self._zombies:
            if zombie.move_index == self._move_index:
                zombie.y = len(self._field[0]) - 1
                self._zombies_in_battle.append(zombie)
                zombies_to_remove.append(zombie)
        for zombie in zombies_to_remove:
            self._zombies.remove(zombie)

    def shoot_at_zombies(self):
        for shooter in self.shooters_list:
            shooter.shooting(self._zombies_in_battle)
        for s_shooter in self.s_shooters_list:
            s_shooter.s_shooting(self._zombies_in_battle, self._field)

    def move_zombies(self):
        for zombie in self._zombies_in_battle:
            zombie.move_zombie()
            if zombie.y == 0:
                return self._move_index + 2
            # deleting dead plants
            for shooter in self.shooters_list + self.s_shooters_list:
                if shooter.get_coords() == zombie.get_coords():
                    if isinstance(shooter, SShooter):
                        self.s_shooters_list.remove(shooter)
                    else:
                        self.shooters_list.remove(shooter)
                    break

    def show_battlefield(self):
        pr_field = [list(i) for i in [[""] * len(self._field[0])] * len(self._field)]
        for zombie in self._zombies_in_battle:
            pr_field[zombie.x][zombie.y] = f"z{zombie.hp}"
        for plant in self.shooters_list + self.s_shooters_list:
            pr_field[plant.x][plant.y] = plant.__str__()
        pprint(pr_field)

    def battle(self):
        """calculating the moves and processing battle between zombies and plants"""

        while self._zombies_in_battle or self._zombies:
            self.set_zombies()

            # self.show_battlefield()
            # print(f"move {self._move_index}")

            # shooting at zombies
            self.shoot_at_zombies()

            # moving our zombies
            move_result = self.move_zombies()

            if move_result is not None:
                return move_result
            self._move_index += 1


def plants_and_zombies(lawn, zombies):
    battle_1 = BattleField(lawn, zombies)
    return battle_1.battle()


lawn = [
    '1         ',
    'SS        ',
    'SSS       ',
    'SSS       ',
    'SS        ',
    '1         ']
zombies = [[0, 2, 16], [1, 3, 19], [2, 0, 18], [4, 2, 21], [6, 3, 20], [7, 5, 17], [8, 1, 21], [8, 2, 11], [9, 0, 10],
           [11, 4, 23], [12, 1, 15], [13, 3, 22]]

print(plants_and_zombies(lawn, zombies))
