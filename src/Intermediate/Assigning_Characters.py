# After that, we are missing to define moves (north, south, east, west), and loading data from saved account

import random

from src.Armor.Weapon import Weapon
from src.Armor.Shield import Shield
from src.Armor.Aid import Aid
from src.Characters.Boss_Enemy import Boss
from src.Characters.Regular_Enemies import Orc
import src.Common_general_functionalities.common_strings as cs


class Assignments:

    """
    This class gets the positions of boss, enemies, aids, level, and data tree (containing data about shields and
    weapons). It creates corresponding boss/enemy/aid for these positions. The way to access the enemy/aid/boss is with
    the get methods, which given a (correct!) position, they return the corresponding enemy/boss/aid. If you
    defeated/collected the enemy/boss/aid, you can remove it/them by using the remove method, which given position,
    it deletes the item from the dictionary.
    """

    def __init__(self, boss_position, enemies_positions, aid_positions, level, data_tree):
        self._enemies = self.initiate_enemies(enemies_positions, level, data_tree)
        self._aids = self.initiate_aids(aid_positions, level)
        self.boss = self.create_boss(data_tree)

    @staticmethod
    def initiate_enemies(enemies_positions, level, data_tree):
        """
        This method will return a dictionary type which maps position to an enemy (Orc). The strength of the enemies
        will be a random function depending on the level.

        NOTE: there is no stop in case the level is high, and we are trying to get a weapon/shield that is too good
        for our data. The program will keep on looking for such an armor that doesn't exist.

        NOTE: for now, also all enemies are not undercover. In order to change that, you must consider changing
        Universe_Construction.

        cs.amount_of_possible_levels
        """
        position_to_enemy = dict()
        for position in enemies_positions:
            weapon_number = random.choice(range(level, level*2 + 1))
            shield_number = random.choice(range(level, level * 2 + 1))
            i = 0
            while weapon_number > 0:
                i += 1
                if not data_tree['Weapons'].search(i):
                    continue
                else:
                    weapon_number -= 1
            current_enemy_weapon = data_tree['Weapons'].search(i)
            i = 0
            while shield_number > 0:
                i += 1
                if not data_tree['Shields'].search(i):
                    continue
                else:
                    shield_number -= 1
            current_enemy_shield = data_tree['Shields'].search(i)
            if not isinstance(current_enemy_weapon, Weapon) or not isinstance(current_enemy_shield, Shield):
                raise ValueError("Problem in the program.")
            position_to_enemy[position] = Orc(random.choice(range(level*10, level*15)), False, current_enemy_weapon, current_enemy_shield)
        return position_to_enemy

    @staticmethod
    def initiate_aids(aids_positions, level):
        """
        This method will return a dictionary type which maps position to an aid. The magnitude of the aid
        will be a random function depending on the level.

        The magnitude of every Aid is currently according to this formula: random.choice(range(1, min(level + 1, cs.amount_of_possible_magnitudes)
        This is not efficient. Please adjust in the future.
        """
        position_to_aid = dict()
        for position in aids_positions:
            chosen_aid = random.choice(cs.aid_types)
            current_aid = Aid(chosen_aid, chosen_aid, random.choice(range(1, min(level + 1, cs.amount_of_possible_magnitudes))))
            if not isinstance(current_aid, Aid):
                raise ValueError("Problem in the program.")
            position_to_aid[position] = current_aid
        return position_to_aid

    def create_boss(self, data_tree):
        """
        The boss is now created as a constant/dummy response to the rest of the enemies created.
        """
        best_weapon_number = 0
        best_shield_number = 0
        highest_life = 0
        for character in self._enemies.values():
            best_weapon_number = max(best_weapon_number, character.weapon.serial_number_int())
            best_shield_number = max(best_shield_number, character.shield.serial_number_int())
            highest_life = max(highest_life, character.life)
        return Boss(highest_life + 5, data_tree['Weapons'].search(best_weapon_number), data_tree['Shields'].search(best_shield_number))

    def get_enemy(self, position):
        if position not in self._enemies.keys():
            return False
        return self._enemies[position]

    def remove_enemy(self, position):
        if position not in self._enemies.keys():
            raise ValueError("You tried to call a position that is not an Enemy position")
        del self._enemies[position]

    def get_aid(self, position):
        if position not in self._aids.keys():
            return False
        return self._aids[position]

    def remove_aid(self, position):
        if position not in self._aids.keys():
            raise ValueError("You tried to call a position that is not an Enemy position")
        del self._aids[position]
