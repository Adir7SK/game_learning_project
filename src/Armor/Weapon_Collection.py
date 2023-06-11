from src.Armor.Weapon import Weapon
from src.Common_general_functionalities.Binary_Tree import AVL


class WeaponCollection:

    def __init__(self, name, weight, material, density, shape, efficient, sound):
        w = Weapon(name, weight, material, density, shape, efficient, sound)
        self.weapon_collection = AVL().insert(None, w.serial_number_int(), w)

    def insert_weapon(self, name, weight, material, density, shape, efficient, sound):
        w = Weapon(name, weight, material, density, shape, efficient, sound)
        self.weapon_collection = AVL().insert(self.weapon_collection, w.serial_number_int(), w)

    def search(self, serial_number):
        return AVL().search(self.weapon_collection, serial_number)

    def best_weapon(self):
        temp_tree = self.weapon_collection
        while temp_tree.right is not None:
            temp_tree = temp_tree.right
        return temp_tree.serial_number

    def worst_weapon(self):
        temp_tree = self.weapon_collection
        while temp_tree.left is not None:
            temp_tree = temp_tree.left
        return temp_tree.serial_number

    def print_helper(self):
        """Call this method as follows: TREE_OBJECT_NAME.print_helper()"""
        AVL().print_helper(self.weapon_collection)
