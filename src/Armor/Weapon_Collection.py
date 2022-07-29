from src.Armor.Weapon import Weapon
from src.Common_general_functionalities.Binary_Tree import AVL
from src.Common_general_functionalities import common_strings as cs


class WeaponCollection:

    def __init__(self, name, weight, material, density, shape, efficient, sound):
        w = Weapon(name, weight, material, density, shape, efficient, sound)
        self.weapon_collection = AVL().insert(None, w.serial_number_int(), w)

    def insert_weapon(self, name, weight, material, density, shape, efficient, sound):
        obj = Weapon(name, weight, material, density, shape, efficient, sound)
        self.weapon_collection = AVL().insert(self.weapon_collection, obj.serial_number_int(), obj)

    def search(self, serial_number):
        return AVL().search(self.weapon_collection, serial_number)

    def print_helper(self):
        """Call this method as follows: TREE_OBJECT_NAME.print_helper()"""
        AVL().print_helper(self.weapon_collection)


if __name__ == "__main__":
    w = WeaponCollection("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom")
    w.insert_weapon("Another Weapon", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh")
    w.insert_weapon("Strong Weapon", 1, cs.iron, 70, cs.slim + " " + cs.even, True, "Baam")
    w.print_helper()
    ww = Weapon("Something", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh")
    print(w.search(ww.serial_number_int()).name())
