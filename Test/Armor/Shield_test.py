import unittest
import pytest
from src.Armor.Shield import Shield
from src.Common_general_functionalities import common_strings as cs

"""
    THE THINGS WE ARE TESTING HERE:
    error when not initiating all required attributes - unittest
    error when initiating with wrong data type - pytest
    error when trying to change an attribute's value - pytest
    all functions are returning a valid value - pytest
"""


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Shield", -2.0, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 0, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Shield", 2.0, "Non-existing material", 10, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Shield", 2.0, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even + " " + cs.even,
                           False, "Woosh"),
                          ("Some Shield", "3", cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, "10", cs.broad + " " + cs.even, True, "Woosh"),
                          ])
def test_initiate_with_wrong_inputs(name, weight, material, density, shape, efficient, sound):
    """
    Validating that we get a value error in the following cases when initiating a Shield object:
    Non-positive weight, non-existing material type, non-positive density, too many shape details, wrong data type for
    weight and density.
    """
    with pytest.raises(ValueError):
        Shield(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Shield", 3, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, 0, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, 1.5, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, "False", "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, "True", "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, None, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_efficient(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating Shield with efficient non-boolean.
    """
    with pytest.raises(TypeError):
        Shield(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [(True, 3, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Woosh"),
                          (0, 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh"),
                          (1.0, 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, False, "Woosh"),
                          (["Some Shield"], 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh"),
                          (None, 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, False, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_name(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating Shield with non-string name.
    """
    with pytest.raises(TypeError):
        Shield(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Shield", "3", cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Shield", True, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Shield", [3], cs.wood_ipe, 50, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Shield", None, cs.wood_ipe, 50, cs.broad + " " + cs.even, False, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_weight(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating Shield with non-numerical value weight.
    """
    with pytest.raises(ValueError):
        Shield(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Shield", 3, True, 10, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Shield", 3, [cs.wood_african_mahogany], 50, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Shield", 3, 5, 50, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Shield", 3, 1.5, 50, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Shield", 3, None, 20, cs.broad + " " + cs.even, True, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_material(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating Shield with non-string material value.
    """
    with pytest.raises(ValueError):
        Shield(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Shield", 3, cs.wood_african_mahogany, "10", cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, True, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, [50], cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, None, cs.broad + " " + cs.even, False, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_density(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating Shield with non-numerical density value.
    """
    with pytest.raises(ValueError):
        Shield(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Shield", 3, cs.wood_african_mahogany, 10, "Non Existing", False, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, 5, True, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, [cs.broad + " " + cs.even], False, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, True, True, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, None, True, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_shape(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating Shield with not realistic shapes.
    """
    with pytest.raises(ValueError):
        Shield(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Shield", 3, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, True),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, ["Woosh"]),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, False, 1),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, 1.5),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, None),
                          ])
def test_initiate_with_wrong_data_type_sound(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating Shield with non-string sound value.
    """
    with pytest.raises(TypeError):
        Shield(name, weight, material, density, shape, efficient, sound)


@pytest.fixture
def ready_shield():
    """Creating an object which we will try to change after initiation."""
    wooden_gun = Shield("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh")
    return wooden_gun


@pytest.mark.parametrize("name_change", [cs.wood_african_mahogany, "Non-existing material", 5, [2, 3], None])
def test_changing_name(ready_shield, name_change):
    """
    Validating that we get attribute error when trying to change the value of name.
    """
    with pytest.raises(AttributeError):
        ready_shield._name = name_change


@pytest.mark.parametrize("weight_change", [cs.wood_african_mahogany, "Non-existing material", 5, [2, 3], True, None])
def test_changing_weight(ready_shield, weight_change):
    """
    Validating that we get attribute error when trying to change the value of weight.
    """
    with pytest.raises(AttributeError):
        ready_shield._weight = weight_change


@pytest.mark.parametrize("material_change", [cs.wood_african_mahogany, "Non-existing material", 5, [2, 3], None])
def test_changing_material(ready_shield, material_change):
    """
    Validating that we get attribute error when trying to change the value of material.
    """
    with pytest.raises(AttributeError):
        ready_shield._material = material_change


@pytest.mark.parametrize("density_change", [cs.wood_african_mahogany, "Non-existing material", 5, [2, 3], 5.5, None])
def test_changing_density(ready_shield, density_change):
    """
    Validating that we get attribute error when trying to change the value of density.
    """
    with pytest.raises(AttributeError):
        ready_shield._density = density_change


@pytest.mark.parametrize("shape_change",
                         [cs.wood_african_mahogany, "Non-existing material", 5, cs.broad + " " + cs.even, None])
def test_changing_shape(ready_shield, shape_change):
    """
    Validating that we get attribute error when trying to change the value of shape.
    """
    with pytest.raises(AttributeError):
        ready_shield._shape = shape_change


@pytest.mark.parametrize("efficient_change", [cs.wood_african_mahogany, True, False, 1, 0, None])
def test_changing_efficient(ready_shield, efficient_change):
    """
    Validating that we get attribute error when trying to change the value of efficient (i.e. Shield's efficiency).
    """
    with pytest.raises(AttributeError):
        ready_shield._efficient = efficient_change


@pytest.mark.parametrize("sound_change", [cs.wood_african_mahogany, "Non-existing material", 5, ["Hello"], None])
def test_changing_sound(ready_shield, sound_change):
    """
    Validating that we get attribute error when trying to change the value of sound.
    """
    with pytest.raises(AttributeError):
        ready_shield._sound = sound_change


@pytest.mark.parametrize("damage", [cs.wood_african_mahogany, "Non-existing material", 5, ["Hello"], True, None])
def test_armor_efficiency_update_type(ready_shield, damage):
    """
    Validating that we get attribute error when trying to update Shield's efficiency with wrong data type.
    """
    with pytest.raises(TypeError):
        ready_shield.armor_efficiency_update(damage)


@pytest.mark.parametrize("damage", [5.2, 1.0, 0.0, -10.5])
def test_armor_efficiency_update_value(ready_shield, damage):
    """
    Validating that we get attribute error when trying to update Shield's efficiency with value out of range.
    """
    with pytest.raises(ValueError):
        ready_shield.armor_efficiency_update(damage)

    """
    In the followings we are checking that the actually functionalities are working and returning the desired numbers.
    """


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Shield", 3, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Hello"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, False, "Baam"),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom"),
                          ])
def test_serial_number_beginning(name, weight, material, density, shape, efficient, sound):
    """
    Validating that the serial number starts with "Shield".
    """
    shield = Shield(name, weight, material, density, shape, efficient, sound)
    assert (shield.serial_number())[:6] == "Shield"


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound, expected",
                         [(
                          "Some Shield", 3, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Hello", 10),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh", -5),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, False, "Baam", 0),
                          ("Some Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom", 10),
                          ])
def test_serial_number(name, weight, material, density, shape, efficient, sound, expected):
    """
    Validating that the serial number makes sense.
    """
    shield = Shield(name, weight, material, density, shape, efficient, sound)
    assert 5001 > shield.serial_number_int() > expected


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound, expected",
                         [("Some Shield", 2.1, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Hello",
                           20),
                          ("Some Shield", 1, cs.wood_ebony, 2, cs.medium_broad + " " + cs.medium_length, True, "Paam",
                           25),
                          ("Some Shield", 6.0, cs.inconel, 40, cs.broad + " " + cs.even, False, "Swoosh", 25),
                          ("Some Shield", 0.5, cs.titanium, 60.5, cs.slim + " " + cs.short, True, "Boom", 30),
                          ])
def test_strength(name, weight, material, density, shape, efficient, sound, expected):
    """
    Validating that strength is within the right range.
    """
    shield = Shield(name, weight, material, density, shape, efficient, sound)
    if shield.efficient():
        assert expected <= shield.strength() <= 50
    else:
        assert 0 < shield.strength() <= expected


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound, damage, repetitions, expected",
                         [("Some Shield", 2.1, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Hello",
                           .4, 5, .07776),
                          ("Some Shield", 1, cs.wood_ebony, 2, cs.medium_broad + " " + cs.medium_length, True, "Paam",
                           .3, 2, .49),
                          ("Some Shield", 6.0, cs.inconel, 40, cs.broad + " " + cs.even, False, "Swoosh", .1, 1, .9),
                          ("Some Shield", 0.5, cs.titanium, 60.5, cs.slim + " " + cs.short, True, "Boom", .5, 2, .25),
                          ])
def test_correct_armor_efficiency_update(name, weight, material, density, shape, efficient, sound, damage, repetitions,
                                         expected):
    """
    Testing that the armor's efficiency is correct after several changes in the efficiency.
    """
    shield = Shield(name, weight, material, density, shape, efficient, sound)
    for _ in range(repetitions):
        shield.armor_efficiency_update(damage)
    assert round(shield.armor_efficiency(), 5) == expected


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound, damage, repetitions",
                         [("Some Shield", 2.1, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Hello",
                           .4, 5),
                          ("Some Shield", 1, cs.wood_ebony, 2, cs.medium_broad + " " + cs.medium_length, True, "Paam",
                           .3, 2),
                          ("Some Shield", 6.0, cs.inconel, 40, cs.broad + " " + cs.even, False, "Swoosh", .1, 1),
                          ("Some Shield", 0.5, cs.titanium, 60.5, cs.slim + " " + cs.short, True, "Boom", .5, 2),
                          ])
def test_renew_armor_efficiency(name, weight, material, density, shape, efficient, sound, damage, repetitions):
    """
    Testing that the armor's efficiency is correct after several changes in the efficiency and then renewing the efficiency.
    """
    shield = Shield(name, weight, material, density, shape, efficient, sound)
    for _ in range(repetitions):
        shield.armor_efficiency_update(damage)
    shield.renew_armor_efficiency()
    assert round(shield.armor_efficiency(), 5) == 1


class ShieldTest(unittest.TestCase):
    """
    Here we are validating that the calculated strength, speed, and serial numbers are of the correct data type, within
    the correct range, and are of the correct proportion with respect to each other.
    """
    wooden_sword = Shield("Wooden broad sword", 1.5, cs.wood_ebony, 35, cs.broad + " " + cs.even, False, "Hello")

    def test_strength_of_wood_sword_within_correct_range(self, armor=wooden_sword):
        """Validating that the strength is smaller than 20 for inefficient wooden shield"""
        self.assertLessEqual(armor.get_strength(), 20)

    def test_missing_data_initiation(self):
        """Initiating object with missing data gives a TypeError"""
        with self.assertRaises(TypeError):
            Shield("Wooden Sword", 1.5, cs.wood_ipe, 35, cs.broad + " " + cs.even)

    def test_name(self, armor=wooden_sword):
        """Validating that we get the name we defined."""
        self.assertEqual(armor.name(), "Wooden broad sword")

    def test_sound(self, armor=wooden_sword):
        """Validating that we get the sound we defined."""
        self.assertEqual(armor.sound(), "Hello")

    def test_weight(self, armor=wooden_sword):
        """Validating that we get the weight we defined."""
        self.assertEqual(armor.weight(), 1.5)

    def test_material(self, armor=wooden_sword):
        """Validating that we get the material we defined."""
        self.assertEqual(armor.material(), cs.wood_ebony)

    def test_density(self, armor=wooden_sword):
        """Validating that we get the density we defined."""
        self.assertEqual(armor.density(), 35)

    def test_shape(self, armor=wooden_sword):
        """Validating that we get the shape we defined."""
        self.assertEqual(armor.shape(), cs.broad + " " + cs.even)

    def test_efficient(self, armor=wooden_sword):
        """Validating that we get the efficient we defined."""
        self.assertEqual(armor.efficient(), False)

    def test_armor_efficiency(self, armor=wooden_sword):
        """Validating that we get the pre-defined armor's efficiency."""
        self.assertEqual(armor.armor_efficiency(), 1)
