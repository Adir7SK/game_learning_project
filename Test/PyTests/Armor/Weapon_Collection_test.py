import pytest
from src.Common_general_functionalities import common_strings as cs
from src.Armor.Weapon_Collection import WeaponCollection
from src.Armor.Weapon import Weapon


"""name, weight, material, density, shape, efficient, sound"""


@pytest.fixture
def full_tree():
    """Creating a weapon data collection fixture which will be in the form of an AVL tree."""
    weapon_collection = WeaponCollection("Low Wooden Gun", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom")
    weapon_collection.insert_weapon("Medium Wooden Sword", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh")
    weapon_collection.insert_weapon("Good Metal Gun", 1, cs.iron, 70, cs.slim + " " + cs.even, True, "Baam")
    weapon_collection.insert_weapon("Medium Wooden Sword Heavy", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh")
    weapon_collection.insert_weapon("Excellent Metal Gun", 0.5, cs.titanium, 99.9, cs.slim + " " + cs.short, True, "HHH")
    weapon_collection.print_helper()
    return weapon_collection


@pytest.mark.parametrize("obj, expected_name",
                         [(Weapon("Medium Wooden Sword", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh"), "Medium Wooden Sword"),
                          (Weapon("Medium Wooden Sword", 5, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh"), "Medium Wooden Sword"),
                          (Weapon("Excellent Metal Gun", 0.5, cs.titanium, 99.9, cs.slim + " " + cs.short, True, "HHH"), "Excellent Metal Gun"),
                          ])
def test_search_on_tree(full_tree, obj, expected_name):
    """Searching a valid existing serial number works."""
    serial_n = obj.serial_number_int()
    print(full_tree.search(serial_n).name())
    assert full_tree.search(serial_n).name() == expected_name
