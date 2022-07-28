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
    weapon_collection.insert_weapon("Medium Wooden Sword", 5, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh")
    weapon_collection.insert_weapon("Excellent Metal Gun", 0.5, cs.titanium, 100, cs.slim + " " + cs.short, True, "HHH")
    weapon_collection.insert_weapon("Medium Wooden Sword", 0.2, cs.wood_ebony, 50, cs.broad + " " + cs.long, False, "Baam")
    return weapon_collection


@pytest.mark.parametrize("serial_n, expected_name",
                         [(Weapon("Medium Wooden Sword", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh").serial_number_int(), "Medium Wooden Sword"),
                          (Weapon("Medium Wooden Sword", 5, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh").serial_number_int(), "Medium Wooden Sword"),
                          (Weapon("Excellent Metal Gun", 0.5, cs.titanium, 100, cs.slim + " " + cs.short, True, "HHH"), "Excellent Metal Gun"),
                          ])
def test_search_on_tree(full_tree, serial_n, expected_name):
    """Searching a valid existing serial number works."""
    assert full_tree.search(serial_n).name == expected_name


@pytest.mark.parametrize("serial_n", [4, 2, 1000, 3])
def test_search_index_that_doesnt_exists(full_tree, serial_n):
    """searching a valid but non-existing serial number returns False."""
    assert AVLTree.search(full_tree, serial_n) is False


@pytest.mark.parametrize("serial_n", [4.5, "2", [1000], {3: 3}])
def test_search_index_with_wrong_data_type(full_tree, serial_n):
    """Searching an invalid serial number raises a Type Error."""
    with pytest.raises(TypeError):
        AVLTree.search(full_tree, serial_n)


@pytest.mark.parametrize("serial_n, input_obj_name",
                         [(4.5, cs.sloppy),
                          ("2", cs.sword),
                          ([1000], cs.efficient),
                          ({3: 3}, "Machine Gun"),
                          ])
def test_insert_invalid_index(full_tree, serial_n, input_obj_name):
    """Insertion with invalid serial number type raises an attribute error."""
    with pytest.raises(AttributeError):
        AVLTree.insert(full_tree, serial_n, BasicObject(input_obj_name))


@pytest.mark.parametrize("serial_n, input_obj",
                         [(4, cs.sloppy),
                          (2, WrongObject(cs.sword)),
                          (1000, [cs.efficient]),
                          (3, 5),
                          ])
def test_insert_invalid_object(full_tree, serial_n, input_obj):
    """Insertion with invalid object raises an attribute error."""
    with pytest.raises(AttributeError):
        AVLTree.insert(full_tree, serial_n, input_obj)
