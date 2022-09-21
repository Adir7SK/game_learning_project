import unittest
import pytest
from src.Armor.Weapon import Weapon
from src.Common_general_functionalities import common_strings as cs

"""
    THE THINGS WE ARE TESTING HERE:
    error when not initiating all required attributes - unittest
    error when initiating with wrong data type - pytest
    error when trying to change an attribute's value - pytest
    all functions are returning a valid value - pytest
"""


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Weapon", -2.0, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 0, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Weapon", 2.0, "Non-existing material", 10, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Weapon", 2.0, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even + " " + cs.even, False, "Woosh"),
                          ("Some Weapon", "3", cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, "10", cs.broad + " " + cs.even, True, "Woosh"),
                          ])
def test_initiate_with_wrong_inputs(name, weight, material, density, shape, efficient, sound):
    """
    Validating that we get a value error in the following cases when initiating a Weapon object:
    Non-positive weight, non-existing material type, non-positive density, too many shape details, wrong data type for
    weight and density.
    """
    with pytest.raises(ValueError):
        Weapon(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Weapon", 3, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, 0, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, 1.5, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, "False", "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, "True", "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, None, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_efficient(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating weapon with efficient non-boolean.
    """
    with pytest.raises(TypeError):
        Weapon(name, weight, material, density, shape, efficient, sound)
        
        
@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [(True, 3, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Woosh"),
                          (0, 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh"),
                          (1.0, 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, False, "Woosh"),
                          (["Some Weapon"], 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh"),
                          (None, 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, False, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_name(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating weapon with non-string name.
    """
    with pytest.raises(TypeError):
        Weapon(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Weapon", "3", cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Weapon", True, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Weapon", [3], cs.wood_ipe, 50, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Weapon", None, cs.wood_ipe, 50, cs.broad + " " + cs.even, False, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_weight(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating weapon with non-numerical value weight.
    """
    with pytest.raises(ValueError):
        Weapon(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Weapon", 3, True, 10, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Weapon", 3, [cs.wood_african_mahogany], 50, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Weapon", 3, 5, 50, cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Weapon", 3, 1.5, 50, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Weapon", 3, None, 20, cs.broad + " " + cs.even, True, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_material(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating weapon with non-string material value.
    """
    with pytest.raises(ValueError):
        Weapon(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Weapon", 3, cs.wood_african_mahogany, "10", cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, True, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, [50], cs.broad + " " + cs.even, False, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, None, cs.broad + " " + cs.even, False, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_density(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating weapon with non-numerical density value.
    """
    with pytest.raises(ValueError):
        Weapon(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Weapon", 3, cs.wood_african_mahogany, 10, "Non Existing", False, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, 5, True, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, [cs.broad + " " + cs.even], False, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, True, True, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, None, True, "Woosh"),
                          ])
def test_initiate_with_wrong_data_type_shape(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating weapon with not realistic shapes.
    """
    with pytest.raises(ValueError):
        Weapon(name, weight, material, density, shape, efficient, sound)


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Weapon", 3, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, True),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, ["Woosh"]),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, False, 1),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, 1.5),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, None),
                          ])
def test_initiate_with_wrong_data_type_sound(name, weight, material, density, shape, efficient, sound):
    """
    Error when initiating weapon with non-string sound value.
    """
    with pytest.raises(TypeError):
        Weapon(name, weight, material, density, shape, efficient, sound)


@pytest.fixture
def ready_weapon():
    """Creating an object which we will try to change after initiation."""
    wooden_gun = Weapon("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh")
    return wooden_gun


@pytest.mark.parametrize("name_change", [cs.wood_african_mahogany, "Non-existing material", 5, [2, 3], None])
def test_changing_name(ready_weapon, name_change):
    """
    Validating that we get attribute error when trying to change the value of name.
    """
    with pytest.raises(AttributeError):
        ready_weapon._name = name_change


@pytest.mark.parametrize("weight_change", [cs.wood_african_mahogany, "Non-existing material", 5, [2, 3], True, None])
def test_changing_weight(ready_weapon, weight_change):
    """
    Validating that we get attribute error when trying to change the value of weight.
    """
    with pytest.raises(AttributeError):
        ready_weapon._weight = weight_change


@pytest.mark.parametrize("material_change", [cs.wood_african_mahogany, "Non-existing material", 5, [2, 3], None])
def test_changing_material(ready_weapon, material_change):
    """
    Validating that we get attribute error when trying to change the value of material.
    """
    with pytest.raises(AttributeError):
        ready_weapon._material = material_change


@pytest.mark.parametrize("density_change", [cs.wood_african_mahogany, "Non-existing material", 5, [2, 3], 5.5, None])
def test_changing_density(ready_weapon, density_change):
    """
    Validating that we get attribute error when trying to change the value of density.
    """
    with pytest.raises(AttributeError):
        ready_weapon._density = density_change


@pytest.mark.parametrize("shape_change", [cs.wood_african_mahogany, "Non-existing material", 5, cs.broad + " " + cs.even, None])
def test_changing_shape(ready_weapon, shape_change):
    """
    Validating that we get attribute error when trying to change the value of shape.
    """
    with pytest.raises(AttributeError):
        ready_weapon._shape = shape_change


@pytest.mark.parametrize("efficient_change", [cs.wood_african_mahogany, True, False, 1, 0, None])
def test_changing_efficient(ready_weapon, efficient_change):
    """
    Validating that we get attribute error when trying to change the value of efficient (i.e. weapon's efficiency).
    """
    with pytest.raises(AttributeError):
        ready_weapon._efficient = efficient_change


@pytest.mark.parametrize("sound_change", [cs.wood_african_mahogany, "Non-existing material", 5, ["Hello"], None])
def test_changing_sound(ready_weapon, sound_change):
    """
    Validating that we get attribute error when trying to change the value of sound.
    """
    with pytest.raises(AttributeError):
        ready_weapon._sound = sound_change


@pytest.mark.parametrize("damage", [cs.wood_african_mahogany, "Non-existing material", 5, ["Hello"], True, None])
def test_armor_efficiency_update_type(ready_weapon, damage):
    """
    Validating that we get attribute error when trying to update weapon's efficiency with wrong data type.
    """
    with pytest.raises(TypeError):
        ready_weapon.armor_efficiency_update(damage)


@pytest.mark.parametrize("damage", [5.2, 1.0, 0.0, -10.5])
def test_armor_efficiency_update_value(ready_weapon, damage):
    """
    Validating that we get attribute error when trying to update weapon's efficiency with value out of range.
    """
    with pytest.raises(ValueError):
        ready_weapon.armor_efficiency_update(damage)

    """
    In the followings we are checking that the actually functionalities are working and returning the desired numbers.
    """


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound",
                         [("Some Weapon", 3, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Hello"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, False, "Baam"),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom"),
                          ])
def test_serial_number_beginning(name, weight, material, density, shape, efficient, sound):
    """
    Validating that the serial number starts with "Weapon".
    """
    weapon = Weapon(name, weight, material, density, shape, efficient, sound)
    assert (weapon.serial_number())[:6] == "Weapon"


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound, expected",
                         [("Some Weapon", 3, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Hello", 10),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Woosh", -5),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, False, "Baam", 0),
                          ("Some Weapon", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom", 10),
                          ])
def test_serial_number(name, weight, material, density, shape, efficient, sound, expected):
    """
    Validating that the serial number makes sense.
    """
    weapon = Weapon(name, weight, material, density, shape, efficient, sound)
    assert 5001 > weapon.serial_number_int() > expected


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound, expected",
                         [("Some Weapon", 2.1, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Hello", 20),
                          ("Some Weapon", 1, cs.wood_ebony, 2, cs.medium_broad + " " + cs.medium_length, True, "Paam", 25),
                          ("Some Weapon", 6.0, cs.inconel, 40, cs.broad + " " + cs.even, False, "Swoosh", 25),
                          ("Some Weapon", 0.5, cs.titanium, 60.5, cs.slim + " " + cs.short, True, "Boom", 30),
                          ])
def test_strength(name, weight, material, density, shape, efficient, sound, expected):
    """
    Validating that strength is within the right range.
    """
    weapon = Weapon(name, weight, material, density, shape, efficient, sound)
    if weapon.efficient():
        assert expected <= weapon.strength() <= 50
    else:
        assert 0 < weapon.strength() <= expected


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound, damage, repetitions, expected",
                         [("Some Weapon", 2.1, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Hello", .4, 5, .07776),
                          ("Some Weapon", 1, cs.wood_ebony, 2, cs.medium_broad + " " + cs.medium_length, True, "Paam", .3, 2, .49),
                          ("Some Weapon", 6.0, cs.inconel, 40, cs.broad + " " + cs.even, False, "Swoosh", .1, 1, .9),
                          ("Some Weapon", 0.5, cs.titanium, 60.5, cs.slim + " " + cs.short, True, "Boom", .5, 2, .25),
                          ])
def test_correct_armor_efficiency_update(name, weight, material, density, shape, efficient, sound, damage, repetitions, expected):
    """
    Testing that the armor's efficiency is correct after several changes in the efficiency.
    """
    weapon = Weapon(name, weight, material, density, shape, efficient, sound)
    for _ in range(repetitions):
        weapon.armor_efficiency_update(damage)
    assert round(weapon.armor_efficiency(), 5) == expected


@pytest.mark.parametrize("name, weight, material, density, shape, efficient, sound, damage, repetitions",
                         [("Some Weapon", 2.1, cs.wood_african_mahogany, 10, cs.broad + " " + cs.even, False, "Hello", .4, 5),
                          ("Some Weapon", 1, cs.wood_ebony, 2, cs.medium_broad + " " + cs.medium_length, True, "Paam", .3, 2),
                          ("Some Weapon", 6.0, cs.inconel, 40, cs.broad + " " + cs.even, False, "Swoosh", .1, 1),
                          ("Some Weapon", 0.5, cs.titanium, 60.5, cs.slim + " " + cs.short, True, "Boom", .5, 2),
                          ])
def test_renew_armor_efficiency(name, weight, material, density, shape, efficient, sound, damage, repetitions):
    """
    Testing that the armor's efficiency is correct after several changes in the efficiency and then renewing the efficiency.
    """
    weapon = Weapon(name, weight, material, density, shape, efficient, sound)
    for _ in range(repetitions):
        weapon.armor_efficiency_update(damage)
    weapon.renew_armor_efficiency()
    assert round(weapon.armor_efficiency(), 5) == 1

        
class WeaponTest(unittest.TestCase):
    """
    Here we are validating that the calculated strength, speed, and serial numbers are of the correct data type, within
    the correct range, and are of the correct proportion with respect to each other.
    """
    wooden_sword = Weapon("Wooden broad sword", 1.5, cs.wood_ebony, 35, cs.broad + " " + cs.even, False, "Hello")

    def test_strength_of_wood_sword_within_correct_range(self, armor=wooden_sword):
        """Validating that the strength is smaller than 20 for inefficient wooden weapon"""
        self.assertLessEqual(armor.get_strength(), 20)

    def test_missing_data_initiation(self):
        """Initiating object with missing data gives a TypeError"""
        with self.assertRaises(TypeError):
            Weapon("Wooden Sword", 1.5, cs.wood_ipe, 35, cs.broad + " " + cs.even)

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

    def test_energy(self, armor=wooden_sword):
        """Validating that we get the pre-defined energy."""
        self.assertEqual(armor.energy(), 100)
