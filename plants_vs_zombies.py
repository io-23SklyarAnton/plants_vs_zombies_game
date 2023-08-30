from units import *
from pprint import pprint

class BattleField:
    def __init__(self, field: list, zombies: list):
        self._field = [list(i) for i in field]
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
                self._field[zombie.x][zombie.y] = zombie
                zombies_to_remove.append(zombie)
        for zombie in zombies_to_remove:
            self._zombies.remove(zombie)

    def shoot_at_zombies(self):
        for shooter in self.shooters_list:
            shooter.shooting(self._zombies_in_battle, self._field)
        for s_shooter in self.s_shooters_list:
            s_shooter.s_shooting(self._zombies_in_battle, self._field)

    def move_zombies(self):
        for zombie in self._zombies_in_battle:
            zombie.move_zombie(self._field)
            if not zombie.y:
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
        pprint(self._field)

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
