from plants_vs_zombies import BattleField


def plants_and_zombies(lawn, zombies):
    battle_1 = BattleField(lawn, zombies)
    return battle_1.battle()


lawn = [
    '2       ',
    '  S     ',
    '21  S   ',
    '13      ',
    '2 3     ']
zombies = [[0, 4, 28], [1, 1, 6], [2, 0, 10], [2, 4, 15], [3, 2, 16], [3, 3, 13]]

print(plants_and_zombies(lawn, zombies))
