import pytest
from src.Common_general_functionalities import common_strings as cs
from src.Armor.Weapon_Collection import WeaponCollection
from src.Armor.Weapon import Weapon


@pytest.fixture
def example_weapon_tree():
    """Creating a weapon data collection fixture which will be in the form of an AVL tree."""
    weapon_collection = WeaponCollection("Low Wooden Gun", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom")
    weapon_collection.insert_weapon("Medium Wooden Sword", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh")
    weapon_collection.insert_weapon("Good Metal Gun", 1, cs.iron, 70, cs.slim + " " + cs.even, True, "Baam")
    weapon_collection.insert_weapon("Medium Wooden Sword Heavy", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh")
    weapon_collection.insert_weapon("MediumMetal Sword Light", 0.15, cs.iron, 50, cs.slim + " " + cs.even, False, "Shiing")
    weapon_collection.insert_weapon("Excellent Metal Gun", 0.5, cs.titanium, 99.9, cs.slim + " " + cs.short, True, "HHH")
    weapon_collection.print_helper()
    return weapon_collection


@pytest.mark.parametrize("weapon_i, expected_name",
                         [(Weapon("Medium Wooden Sword", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh"), "Medium Wooden Sword"),
                          (Weapon("Medium Wooden Sword", 1, cs.iron, 70, cs.slim + " " + cs.even, True, "Woooh"), "Good Metal Gun"),
                          (Weapon("Excellent Metal Gun", 0.5, cs.titanium, 99.9, cs.slim + " " + cs.short, True, "HHH"), "Excellent Metal Gun"),
                          (Weapon("Excellent Metal Gun", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "HHH"), "Medium Wooden Sword Heavy"),
                          (Weapon("Excellent Metal Gun", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "HHH"), "Low Wooden Gun"),
                          (Weapon("Excellent Metal Gun", 0.15, cs.iron, 50, cs.slim + " " + cs.even, False, "HHH"), "MediumMetal Sword Light"),
                          ])
def test_search_on_tree(example_weapon_tree, weapon_i, expected_name):
    """
    Here we are testing 2 things:
    1. Searching an existing weapon (by serial number) in the weapon data structure works.
    2. When creating a new weapon with the same serial number as another weapon in the data, will not interfere with the
       existing data.
    The test cases are searching for all weapons in the tree, one at a time.
    """
    serial_n = weapon_i.serial_number_int()
    assert example_weapon_tree.search(serial_n).name() == expected_name


@pytest.mark.parametrize("weapon_i",
                         [(Weapon("Medium Wooden Sword", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh")),
                          (Weapon("Medium Wooden Sword", 1, cs.iron, 70, cs.slim + " " + cs.even, True, "Woooh")),
                          ])
def test_cannot_insert_weapon_with_same_serial_number(example_weapon_tree, weapon_i):
    """Ensuring that an object with a serial number similar to another one cannot be added to the weapon collection."""
    with pytest.raises(ValueError):
        example_weapon_tree.insert_weapon(weapon_i.name(), weapon_i.weight(), weapon_i.material(), weapon_i.density(),
                                          weapon_i.shape(), weapon_i.efficient(), weapon_i.sound())


@pytest.mark.parametrize("weapon_i",
                         [(Weapon("Bad Weapon", 25, cs.wood_ebony, 1, cs.medium_length + " " + cs.even, False, "Woosh")),
                          (Weapon("Strong Weapon", 0.1, cs.titanium, 1, cs.broad + " " + cs.even, True, "Baam")),
                          ])
def test_can_insert_weapon_with_different_serial_number_after_tree_is_created(example_weapon_tree, weapon_i):
    """Showing it is possible to insert new weapons to the tree."""
    example_weapon_tree.insert_weapon(weapon_i.name(), weapon_i.weight(), weapon_i.material(), weapon_i.density(),
                                      weapon_i.shape(), weapon_i.efficient(), weapon_i.sound())


@pytest.mark.parametrize("args",
                         [(["Medium Wooden Sword", 1, cs.wood_african_mahogany, 2000, cs.slim + " " + cs.even]),
                          (["Medium Wooden Sword", 1, cs.wood_ipe, 70, cs.slim + " " + cs.even, True]),
                          ])
def test_error_inserting_directly_weapon_with_missing_details(example_weapon_tree, args):
    """Validation that we get an error when creating weapon with missing data."""
    with pytest.raises(TypeError):
        if len(args) == 5:
            example_weapon_tree.insert_weapon(args[0], args[1], args[2], args[3], args[4])
        elif len(args) == 6:
            example_weapon_tree.insert_weapon(args[0], args[1], args[2], args[3], args[4], args[5])


@pytest.mark.parametrize("args",
                         [([5, 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh"]),
                          (["Excellent Metal Gun", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, "True", "HHH"]),
                          (["Excellent Metal Gun", 0.15, cs.iron, 50, cs.slim + " " + cs.even, False, 0]),
                          ])
def test_type_error_inserting_directly_weapon_with_wrong_data_types(example_weapon_tree, args):
    """Verifying that the validation process from Weapon class applies here."""
    with pytest.raises(TypeError):
        example_weapon_tree.insert_weapon(args[0], args[1], args[2], args[3], args[4], args[5], args[6])


@pytest.mark.parametrize("args",
                         [(["Medium Wooden Sword", 1, 5, 20, cs.slim + " " + cs.even, False, "Woosh"]),
                          (["Medium Wooden Sword", "1", cs.iron, 70, cs.slim + " " + cs.even, True, "Woooh"]),
                          (["Medium Wooden Sword", 1, cs.iron, "70", cs.slim + " " + cs.even, True, "Woooh"]),
                          (["Excellent Metal Gun", 3, cs.wood_african_mahogany, 50, 5, True, "HHH"]),
                          ])
def test_value_error_inserting_directly_weapon_with_wrong_data_types(example_weapon_tree, args):
    """Verifying that the validation process from Weapon class applies here."""
    with pytest.raises(ValueError):
        example_weapon_tree.insert_weapon(args[0], args[1], args[2], args[3], args[4], args[5], args[6])


@pytest.mark.parametrize("class_method, value",
                         [("name", "Hi"),
                          ("name", 4),
                          ("weight", 5),
                          ("weight", "3"),
                          ("material", cs.wood_african_mahogany),
                          ("material", None),
                          ("density", 20),
                          ("density", "h"),
                          ("shape", cs.slim + " " + cs.even),
                          ("shape", None),
                          ("efficient", True),
                          ("efficient", None),
                          ("sound", "Bom"),
                          ("sound", 10),
                         ])
def test_error_when_trying_to_change_existing_weapon(example_weapon_tree, class_method, value):
    """Verifying that the validation process from Weapon applies here."""
    serial_number = 460
    with pytest.raises(AttributeError):
        if class_method == "name":
            example_weapon_tree.search(serial_number)._name = value
        elif class_method == "weight":
            example_weapon_tree.search(serial_number)._weight = value
        elif class_method == "material":
            example_weapon_tree.search(serial_number)._material = value
        elif class_method == "density":
            example_weapon_tree.search(serial_number)._density = value
        elif class_method == "shape":
            example_weapon_tree.search(serial_number)._shape = value
        elif class_method == "efficient":
            example_weapon_tree.search(serial_number)._efficient = value
        elif class_method == "sound":
            example_weapon_tree.search(serial_number)._sound = value


@pytest.mark.parametrize("serial_number", [1, 333, -10])
def test_searching_non_existing_serial_number_returns_false(example_weapon_tree, serial_number):
    """Verifying that the validation process from AVL data type applies here."""
    assert example_weapon_tree.search(serial_number) is False


@pytest.mark.parametrize("serial_n", [4.5, "2", [1000], {3: 3}])
def test_search_invalid_serial_number_data_type_raises_type_error(example_weapon_tree, serial_n):
    """Searching an invalid serial number raises a Type Error."""
    with pytest.raises(TypeError):
        example_weapon_tree.search(serial_n)
