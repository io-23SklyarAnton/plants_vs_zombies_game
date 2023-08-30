from typing import List
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
        return f"z{self.hp}"

    def __str__(self):
        return f"z{self.hp}"

    def move_zombie(self, field):
        field[self.x][self.y] = " "
        self.y -= 1
        field[self.x][self.y] = self


class Shooter(Unit):
    def __init__(self, x: int, y: int, power: int = 1):
        super().__init__(x, y)
        self.power = power

    def __repr__(self):
        return f"Plant at ({self.x}, {self.y}) coord"

    def __str__(self):
        return f"{self.power}"

    def shooting(self, zombie_list: List[Zombie], field):
        current_shots = self.power
        for y in range(self.y, len(field[0])):
            if isinstance(field[self.x][y], Zombie):
                zombie = field[self.x][y]
                zombie.hp, current_shots = zombie.hp - current_shots, current_shots - zombie.hp
                if zombie.hp <= 0:
                    field[zombie.x][zombie.y] = " "
                    zombie_list.remove(zombie)
                if current_shots <= 0:
                    break


class SShooter(Shooter):
    def __init__(self, x, y):
        super().__init__(x, y)

    def __str__(self):
        return "S"

    def s_shooting(self, zombie_list: List[Zombie], field: list):
        zombies_under_fire = []
        row_len = len(field[0])
        column_len = len(field)

        for y in range(self.y, row_len):
            if isinstance(field[self.x][y], Zombie):
                zombies_under_fire.append(field[self.x][y])
                break
        try:
            for x, y in enumerate(range(self.y, row_len), self.x):
                if isinstance(field[x][y], Zombie):
                    zombies_under_fire.append(field[x][y])
                    break
        except IndexError:
            pass
        try:
            for y, x in enumerate(range(self.x, -1, -1), self.y):
                if isinstance(field[x][y], Zombie):
                    zombies_under_fire.append(field[x][y])
                    break
        except IndexError:
            pass

        for zombie in zombies_under_fire:
            zombie.hp -= 1
            if zombie.hp <= 0:
                field[zombie.x][zombie.y] = " "
                zombie_list.remove(zombie)


