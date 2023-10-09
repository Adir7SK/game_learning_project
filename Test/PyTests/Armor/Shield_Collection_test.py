import pytest
from src.Common_general_functionalities import common_strings as cs
from src.Armor.Shield_Collection import ShieldCollection
from src.Armor.Shield import Shield


@pytest.fixture
def example_shield_tree():
    """Creating a shield data collection fixture which will be in the form of an AVL tree."""
    shield_collection = ShieldCollection("Low Wooden Body Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom")
    shield_collection.insert_shield("Medium Wooden Hand Shield", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh")
    shield_collection.insert_shield("Good Metal Body Shield", 1, cs.iron, 70, cs.slim + " " + cs.even, True, "Baam")
    shield_collection.insert_shield("Medium Wooden Hand Shield Heavy", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh")
    shield_collection.insert_shield("MediumMetal Hand Shield Light", 0.15, cs.iron, 50, cs.slim + " " + cs.even, False, "Shiing")
    shield_collection.insert_shield("Excellent Metal Body Shield", 0.5, cs.titanium, 99.9, cs.slim + " " + cs.short, True, "HHH")
    shield_collection.print_helper()
    return shield_collection


@pytest.mark.parametrize("shield_i, expected_name",
                         [(Shield("Medium Wooden Hand Shield", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh"), "Medium Wooden Hand Shield"),
                          (Shield("Medium Wooden Hand Shield", 1, cs.iron, 70, cs.slim + " " + cs.even, True, "Woooh"), "Good Metal Body Shield"),
                          (Shield("Excellent Metal Body Shield", 0.5, cs.titanium, 99.9, cs.slim + " " + cs.short, True, "HHH"), "Excellent Metal Body Shield"),
                          (Shield("Excellent Metal Body Shield", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "HHH"), "Medium Wooden Hand Shield Heavy"),
                          (Shield("Excellent Metal Body Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "HHH"), "Low Wooden Body Shield"),
                          (Shield("Excellent Metal Body Shield", 0.15, cs.iron, 50, cs.slim + " " + cs.even, False, "HHH"), "MediumMetal Hand Shield Light"),
                          ])
def test_search_on_tree(example_shield_tree, shield_i, expected_name):
    """
    Here we are testing 2 things:
    1. Searching an existing shield (by serial number) in the shield data structure works.
    2. When creating a new shield with the same serial number as another shield in the data, will not interfere with the
       existing data.
    The test cases are searching for all shields in the tree, one at a time.
    """
    serial_n = shield_i.serial_number_int()
    assert example_shield_tree.search(serial_n).name() == expected_name


@pytest.mark.parametrize("shield_i",
                         [(Shield("Medium Wooden Hand Shield", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh")),
                          (Shield("Medium Wooden Hand Shield", 1, cs.iron, 70, cs.slim + " " + cs.even, True, "Woooh")),
                          ])
def test_cannot_insert_shield_with_same_serial_number(example_shield_tree, shield_i):
    """Ensuring that an object with a serial number similar to another one cannot be added to the shield collection."""
    copy_tree = example_shield_tree
    example_shield_tree.insert_shield(shield_i.name(), shield_i.weight(), shield_i.material(), shield_i.density(),
                                          shield_i.shape(), shield_i.efficient(), shield_i.sound())
    assert copy_tree == example_shield_tree


@pytest.mark.parametrize("shield_i",
                         [(Shield("Bad Shield", 25, cs.wood_ebony, 1, cs.medium_length + " " + cs.even, False, "Woosh")),
                          (Shield("Strong Shield", 0.1, cs.titanium, 1, cs.broad + " " + cs.even, True, "Baam")),
                          ])
def test_can_insert_shield_with_different_serial_number_after_tree_is_created(example_shield_tree, shield_i):
    """Showing it is possible to insert new shields to the tree."""
    example_shield_tree.insert_shield(shield_i.name(), shield_i.weight(), shield_i.material(), shield_i.density(),
                                      shield_i.shape(), shield_i.efficient(), shield_i.sound())


@pytest.mark.parametrize("args",
                         [(["Medium Wooden Hand Shield", 1, cs.wood_african_mahogany, 2000, cs.slim + " " + cs.even]),
                          (["Medium Wooden Hand Shield", 1, cs.wood_ipe, 70, cs.slim + " " + cs.even, True]),
                          ])
def test_error_inserting_directly_shield_with_missing_details(example_shield_tree, args):
    """Validation that we get an error when creating shield with missing data."""
    with pytest.raises(TypeError):
        if len(args) == 5:
            example_shield_tree.insert_shield(args[0], args[1], args[2], args[3], args[4])
        elif len(args) == 6:
            example_shield_tree.insert_shield(args[0], args[1], args[2], args[3], args[4], args[5])


@pytest.mark.parametrize("args",
                         [([5, 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh"]),
                          (["Excellent Metal Body Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, "True", "HHH"]),
                          (["Excellent Metal Body Shield", 0.15, cs.iron, 50, cs.slim + " " + cs.even, False, 0]),
                          ])
def test_type_error_inserting_directly_shield_with_wrong_data_types(example_shield_tree, args):
    """Verifying that the validation process from Shield class applies here."""
    with pytest.raises(TypeError):
        example_shield_tree.insert_shield(args[0], args[1], args[2], args[3], args[4], args[5], args[6])


@pytest.mark.parametrize("args",
                         [(["Medium Wooden Hand Shield", 1, 5, 20, cs.slim + " " + cs.even, False, "Woosh"]),
                          (["Medium Wooden Hand Shield", "1", cs.iron, 70, cs.slim + " " + cs.even, True, "Woooh"]),
                          (["Medium Wooden Hand Shield", 1, cs.iron, "70", cs.slim + " " + cs.even, True, "Woooh"]),
                          (["Excellent Metal Body Shield", 3, cs.wood_african_mahogany, 50, 5, True, "HHH"]),
                          ])
def test_value_error_inserting_directly_shield_with_wrong_data_types(example_shield_tree, args):
    """Verifying that the validation process from Shield class applies here."""
    with pytest.raises(ValueError):
        example_shield_tree.insert_shield(args[0], args[1], args[2], args[3], args[4], args[5], args[6])


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
def test_error_when_trying_to_change_existing_shield(example_shield_tree, class_method, value):
    """Verifying that the validation process from Shield applies here."""
    serial_number = 460
    with pytest.raises(AttributeError):
        if class_method == "name":
            example_shield_tree.search(serial_number)._name = value
        elif class_method == "weight":
            example_shield_tree.search(serial_number)._weight = value
        elif class_method == "material":
            example_shield_tree.search(serial_number)._material = value
        elif class_method == "density":
            example_shield_tree.search(serial_number)._density = value
        elif class_method == "shape":
            example_shield_tree.search(serial_number)._shape = value
        elif class_method == "efficient":
            example_shield_tree.search(serial_number)._efficient = value
        elif class_method == "sound":
            example_shield_tree.search(serial_number)._sound = value


@pytest.mark.parametrize("serial_number", [1, 333, -10])
def test_searching_non_existing_serial_number_returns_false(example_shield_tree, serial_number):
    """Verifying that the validation process from AVL data type applies here."""
    assert example_shield_tree.search(serial_number) is False


@pytest.mark.parametrize("serial_n", [4.5, "2", [1000], {3: 3}])
def test_search_invalid_serial_number_data_type_raises_type_error(example_shield_tree, serial_n):
    """Searching an invalid serial number raises a Type Error."""
    with pytest.raises(TypeError):
        example_shield_tree.search(serial_n)


@pytest.mark.parametrize("expected", [5000])
def test_best_shield(example_shield_tree, expected):
    """Verifying that the method gives the correct best shield."""
    assert example_shield_tree.best_shield() == expected


@pytest.mark.parametrize("expected", [398])
def test_worst_shield(example_shield_tree, expected):
    """Verifying that the method gives the correct worst shield."""
    assert example_shield_tree.worst_shield() == expected
