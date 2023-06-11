import random

from src.Armor.Weapon import Weapon
from src.Armor.Shield import Shield
from src.Armor.Aid import Aid
from src.Characters.Boss_Enemy import Boss
from src.Characters.Regular_Enemies import Orc
import src.Common_general_functionalities.common_strings as cs
from src.Common_general_functionalities.Gaussian_generated_data import scaled_data


class Assignments:

    """
    This class gets the positions of boss, enemies, aids, level, and data tree (containing data about shields and
    weapons). It creates corresponding boss/enemy/aid for these positions (including their armors and all their details).
    The way to access the enemy/aid/boss is with the get methods, which given a (correct!) position, they return the
    corresponding enemy/boss/aid. If you defeated/collected the enemy/boss/aid, you can remove it/them by using the
    remove method, which given position, it deletes the item from the dictionary.
    init methods immediately creates all the enemies and aids, and assigns them to the correct position.
    get_enemy and get_aid returns the enemy/aid given its position.
    remove_enemy and remove_aid removes them from the list of existing enemies/aids given the correct position.
    You must also provide the strongest and weakest armor used by the enemies in the previous round (the strongest armor
    is easy to get - it is the Boss' armor.
    """

    def __init__(self, enemies_positions, aid_positions, level, data_tree, last_round_weakest_armor=(0, 0),
                 last_round_strongest_armor=(0, 0)):
        if type(enemies_positions) != list or \
                [e for e in enemies_positions if type(e) != tuple or len(e) != 2 or type(e[0]) != int or
                                                 type(e[1]) != int] or type(aid_positions) != list or \
                [e for e in aid_positions if type(e) != tuple or len(e) != 2 or
                 type(e[0]) != int or type(e[1]) != int] or type(level) != int or type(data_tree) != dict or \
                type(last_round_weakest_armor) != tuple or type(last_round_weakest_armor[0]) != int or \
                type(last_round_weakest_armor[1]) != int or type(last_round_strongest_armor) != tuple or \
                type(last_round_strongest_armor[0]) != int or type(last_round_strongest_armor[1]) != int or \
                len(last_round_weakest_armor) != 2 or len(last_round_strongest_armor) != 2:
            raise ValueError("Either enemies_positions, aid_positions, level, data_tree, last_round_weakest_armor or "
                             "last_round_strongest_armor is from the wrong data type")
        self._enemies = self._initiate_enemies(enemies_positions, level, data_tree, last_round_weakest_armor, last_round_strongest_armor)
        self._aids = self._initiate_aids(aid_positions, level)
        self.boss = self.create_boss(data_tree)

    @staticmethod
    def _initiate_enemies(enemies_positions, level, data_tree, last_round_weakest_armor, last_round_strongest_armor):
        """
        This method will return a dictionary type which maps position to an enemy (Orc). The strength of the enemies
        will be a random function depending on the level.
        """
        # The following lines are solely to create the correct possible_weapons and possible_shields
        if last_round_weakest_armor[0] == last_round_strongest_armor[0] != 0:
            average_weapon = int((last_round_weakest_armor[0] + data_tree["Weapons"].best_weapon()) / 2)
            average_shield = int((last_round_weakest_armor[1] + data_tree["Shields"].best_shield()) / 2)
        elif last_round_weakest_armor[0] == 0:
            average_weapon = 0
            average_shield = 0
        else:
            average_weapon = int((last_round_weakest_armor[0]+last_round_strongest_armor[0])/2)
            average_shield = int((last_round_weakest_armor[1]+last_round_strongest_armor[1])/2)
        percentage_above = 1.1
        upper_limit = max(int(average_weapon*percentage_above),
                          int(data_tree["Weapons"].best_weapon()*(percentage_above-1)))
        while len([serial_n for serial_n in range(average_weapon, upper_limit) if
                   data_tree["Weapons"].search(serial_n)]) < 2 and average_weapon < data_tree["Weapons"].best_weapon():
            percentage_above += .05
            upper_limit = max(int(average_weapon * percentage_above),
                              int(data_tree["Weapons"].best_weapon() * (percentage_above - 1)))
        possible_weapons = [serial_n for serial_n in range(average_weapon, upper_limit) if
                            data_tree["Weapons"].search(serial_n)]
        possible_shields = [serial_n for serial_n in range(average_shield, upper_limit) if
                            data_tree["Shields"].search(serial_n)]
        position_to_enemy = dict()
        normal_data = sorted(scaled_data)
        for position in enemies_positions:
            random_w = random.choice(normal_data)
            random_s = random.choice(normal_data)
            e_w = int(len(normal_data)/len(possible_weapons))
            e_s = int(len(normal_data)/len(possible_shields))
            current_enemy_weapon = data_tree["Weapons"].search([possible_weapons[i] for i in
                                                                range(len(possible_weapons)) if
                                                                random_w in normal_data[i*e_w:(i+1)*e_w]][0])
            current_enemy_shield = data_tree["Shields"].search([possible_shields[i] for i in
                                                                range(len(possible_shields)) if
                                                                random_s in normal_data[i*e_s:(i+1)*e_s]][0])
            if not isinstance(current_enemy_weapon, Weapon) or not isinstance(current_enemy_shield, Shield):
                raise ValueError("Problem in the program.")
            position_to_enemy[position] = Orc(random.choice(range(level*10, level*15)), random.choice([True, False]),
                                              current_enemy_weapon, current_enemy_shield)
        return position_to_enemy

    @staticmethod
    def _initiate_aids(aids_positions, level):
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
        return Boss(highest_life*1.1, data_tree['Weapons'].search(best_weapon_number), data_tree['Shields'].search(best_shield_number))

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
