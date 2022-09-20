from src.Armor.Shield import Shield
from src.Common_general_functionalities.Binary_Tree import AVL


class ShieldCollection:

    def __init__(self, name, weight, material, density, shape, efficient, sound):
        sh = Shield(name, weight, material, density, shape, efficient, sound)
        self.shield_collection = AVL().insert(None, sh.serial_number_int(), sh)

    def insert_shield(self, name, weight, material, density, shape, efficient, sound):
        sh = Shield(name, weight, material, density, shape, efficient, sound)
        self.shield_collection = AVL().insert(self.shield_collection, sh.serial_number_int(), sh)

    def search(self, serial_number):
        return AVL().search(self.shield_collection, serial_number)

    def print_helper(self):
        """Call this method as follows: TREE_OBJECT_NAME.print_helper()"""
        AVL().print_helper(self.shield_collection)
