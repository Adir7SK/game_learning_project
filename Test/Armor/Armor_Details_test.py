import unittest
import pytest
from src.Armor.Armor_Details import ArmorDetails
from src.Common_general_functionalities import common_strings as cs

"""
The tests we are doing are split between pytest and unittests. 

With pytest we are testing:
Errors when initiating the object with illegal inputs.
Error when trying to change values after constructing the object.

With unittest we are testing:
Validating that we get values for strength, speed and serial_number within the correct range.
Validating that strength, speed and serial_number have the correct proportion with respect to itself.
Validating that all output values are of the correct data type.
Error when trying to initiate with incomplete data.
"""


@pytest.mark.parametrize("material, weight, density, shape, efficient",
                         [(cs.wood_african_mahogany, -2.0, 10, cs.broad + " " + cs.even, False),
                          (cs.wood_african_mahogany, 3, 0, cs.broad + " " + cs.even, False),
                          ("Non-existing material", 2.0, 10, cs.broad + " " + cs.even, False),
                          (cs.wood_african_mahogany, 2.0, 10, cs.broad + " " + cs.even + " " + cs.even, False),
                          (cs.wood_african_mahogany, "3", 10, cs.broad + " " + cs.even, True),
                          (cs.wood_african_mahogany, 3, "10", cs.broad + " " + cs.even, True),
                          ])
def test_initiate_with_wrong_inputs(material, weight, density, shape, efficient):
    """
    Validating that we get a value error in the following cases when initiating an ArmorDetails object:
    Non-positive weight, non-positive density, non-existing material type, too many shape details, wrong data type for
    weight and density.
    """
    with pytest.raises(ValueError):
        ArmorDetails(material, weight, density, shape, efficient)


@pytest.mark.parametrize("material, weight, density, shape, efficient",
                         [(cs.wood_african_mahogany, 2.0, 10, cs.broad + " " + cs.even, 0),
                          (cs.wood_african_mahogany, 3, 50, cs.broad + " " + cs.even, 1),
                          (cs.wood_african_mahogany, 3, 50, cs.broad + " " + cs.even, "False"),
                          ])
def test_initiate_with_wrong_data_type(material, weight, density, shape, efficient):
    """
    Validating that we get type error when initiating an ArmorDetails object with non-boolean value for
    efficient attribute.
    """
    with pytest.raises(TypeError):
        ArmorDetails(material, weight, density, shape, efficient)


@pytest.fixture
def ready_armor():
    """Creating a few objects which we will try to change after initiation."""
    wooden_sword = ArmorDetails(cs.wood_african_mahogany, 2.0, 10, cs.broad + " " + cs.even, False)
    return wooden_sword


@pytest.mark.parametrize("material_change", [cs.wood_african_mahogany, "Non-existing material", 5, [2, 3]])
def test_changing_material(ready_armor, material_change):
    """
    Validating that we get attribute error when trying to change the value of material.
    """
    with pytest.raises(AttributeError):
        ready_armor._material = material_change


@pytest.mark.parametrize("weight_change", [cs.wood_african_mahogany, .2, 5, [2, 3]])
def test_changing_weight(ready_armor, weight_change):
    """
    Validating that we get attribute error when trying to change the value of weight.
    """
    with pytest.raises(AttributeError):
        ready_armor._weight = weight_change


@pytest.mark.parametrize("density_change", [cs.wood_african_mahogany, .2, 5, [2, 3]])
def test_changing_density(ready_armor, density_change):
    """
    Validating that we get attribute error when trying to change the value of density.
    """
    with pytest.raises(AttributeError):
        ready_armor._density = density_change


@pytest.mark.parametrize("shape_change", [cs.wood_african_mahogany, 3.2, 5, cs.broad + " " + cs.even])
def test_changing_shape(ready_armor, shape_change):
    """
    Validating that we get attribute error when trying to change the value of shape.
    """
    with pytest.raises(AttributeError):
        ready_armor._shape = shape_change


@pytest.mark.parametrize("efficient_change", ["True", True, 0, 1])
def test_changing_efficient(ready_armor, efficient_change):
    """
    Validating that we get attribute error when trying to change the value of shape.
    """
    with pytest.raises(AttributeError):
        ready_armor._efficient = efficient_change


class ArmorDetailsStrengthSpeedSerialNumberTest(unittest.TestCase):
    """
    Here we are validating that the calculated strength, speed, and serial numbers are of the correct data type, within
    the correct range, and are of the correct proportion with respect to each other.
    """
    wooden_sword = ArmorDetails(cs.wood_african_mahogany, 2.0, 10, cs.broad + " " + cs.even, False)
    wooden_gun = ArmorDetails(cs.wood_ebony, 1, 2, cs.medium_broad + " " + cs.medium_length, True)
    wooden_hand_shield = ArmorDetails(cs.wood_ipe, 7.0, 20, cs.slim + " " + cs.short, False)
    wooden_body_shield = ArmorDetails(cs.wood_apple, 4, 10.0, cs.medium_broad + " " + cs.medium_length, True)
    metal_sword = ArmorDetails(cs.inconel, 6.0, 40, cs.broad + " " + cs.even, False)
    metal_gun = ArmorDetails(cs.titanium, 0.5, 60.0, cs.slim + " " + cs.short, True)
    metal_hand_shield = ArmorDetails(cs.iron, 10, 50.0, cs.medium_broad + " " + cs.even, False)
    metal_body_shield = ArmorDetails(cs.steel, 1.0, 70, cs.slim + " " + cs.even, True)

    def test_strength_of_wood_sword_within_correct_range(self, armor=wooden_sword):
        """Validating that the strength is smaller than 20 for inefficient wooden weapon"""
        self.assertLessEqual(armor.get_strength(), 20)

    def test_strength_of_wood_gun_within_correct_range(self, armor=wooden_gun):
        """Validating that the strength is greater than 25 for efficient weapon"""
        self.assertGreaterEqual(armor.get_strength(), 25)

    def test_strength_of_wood_hand_shield_within_correct_range(self, armor=wooden_hand_shield):
        """Validating that the strength is smaller than 20 for inefficient wooden weapon"""
        self.assertLessEqual(armor.get_strength(), 20)

    def test_strength_of_wood_body_shield_within_correct_range(self, armor=wooden_body_shield):
        """Validating that the strength is greater than 25 for efficient weapon"""
        self.assertGreaterEqual(armor.get_strength(), 25)

    def test_strength_of_metal_sword_within_correct_range(self, armor=metal_sword):
        """Validating that the strength is smaller than 25 for inefficient metal weapon"""
        self.assertLessEqual(armor.get_strength(), 25)

    def test_strength_of_metal_gun_within_correct_range(self, armor=metal_gun):
        """Validating that the strength is greater than 30 for efficient metal weapon"""
        self.assertGreaterEqual(armor.get_strength(), 30)

    def test_strength_of_metal_hand_shield_within_correct_range(self, armor=metal_hand_shield):
        """Validating that the strength is smaller than 25 for inefficient metal weapon"""
        self.assertLessEqual(armor.get_strength(), 25)

    def test_strength_of_metal_body_shield_within_correct_range(self, armor=metal_body_shield):
        """Validating that the strength is greater than 30 for efficient metal weapon"""
        self.assertGreaterEqual(armor.get_strength(), 30)

    def test_speed_of_wood_sword_within_correct_range(self, armor=wooden_sword):
        """Validating that the speed is smaller than 5 for inefficient wooden weapon"""
        self.assertLessEqual(armor.get_speed(), 5)

    def test_speed_of_wood_gun_within_correct_range(self, armor=wooden_gun):
        """Validating that the speed is greater than 5 for efficient weapon"""
        self.assertGreaterEqual(armor.get_speed(), 5)

    def test_speed_of_wood_hand_shield_within_correct_range(self, armor=wooden_hand_shield):
        """Validating that the speed is smaller than 5 for inefficient wooden weapon"""
        self.assertLessEqual(armor.get_speed(), 5)

    def test_speed_of_wood_body_shield_within_correct_range(self, armor=wooden_body_shield):
        """Validating that the speed is greater than 5 for efficient weapon"""
        self.assertGreaterEqual(armor.get_speed(), 5)

    def test_speed_of_metal_sword_within_correct_range(self, armor=metal_sword):
        """Validating that the speed is smaller than 5 for inefficient metal weapon"""
        self.assertLessEqual(armor.get_speed(), 5)

    def test_speed_of_metal_gun_within_correct_range(self, armor=metal_gun):
        """Validating that the speed is greater than 5 for efficient metal weapon"""
        self.assertGreaterEqual(armor.get_speed(), 5)

    def test_speed_of_metal_hand_shield_within_correct_range(self, armor=metal_hand_shield):
        """Validating that the speed is smaller than 5 for inefficient metal weapon"""
        self.assertLessEqual(armor.get_speed(), 5)

    def test_speed_of_metal_body_shield_within_correct_range(self, armor=metal_body_shield):
        """Validating that the speed is greater than 5 for efficient metal weapon"""
        self.assertGreaterEqual(armor.get_speed(), 5)

    def test_serial_number_shield_comparison(self, wood_armor=wooden_body_shield, metal_armor=metal_body_shield):
        """Validating that the serial number (sn) of a metal armor is greater than the sn of the same armor in wood"""
        self.assertGreater(metal_armor.get_serial_number(), wood_armor.get_serial_number())

    def test_serial_number_weapon_comparison(self, wood_armor=wooden_gun, metal_armor=metal_gun):
        """Validating that the serial number (sn) of a metal armor is greater than the sn of the same armor in wood"""
        self.assertGreater(metal_armor.get_serial_number(), wood_armor.get_serial_number())

    def test_serial_number_weak_strong_weapon_comparison(self, weak_armor=metal_sword, strong_armor=wooden_gun):
        """Validating that the serial number (sn) of efficient weapon is greater than the sn of non-efficient weapon"""
        self.assertGreater(strong_armor.get_serial_number(), weak_armor.get_serial_number())

    def test_serial_number_weak_strong_shield_comparison(self, weak_armor=wooden_hand_shield,
                                                         strong_armor=metal_body_shield):
        """Validating that the serial number (sn) of efficient shield is greater than the sn of non-efficient shield"""
        self.assertGreater(strong_armor.get_serial_number(), weak_armor.get_serial_number())

    def test_data_type_of_serial_numbers(self, wws=wooden_sword, wwg=wooden_gun, swh=wooden_hand_shield,
                                         swb=wooden_body_shield, wms=metal_sword, wmg=metal_gun,
                                         smh=metal_hand_shield, smb=metal_body_shield):
        """Validating that all serial numbers are int data types"""
        serial_numbers_sum_type = wws.get_serial_number() + wwg.get_serial_number() + swh.get_serial_number() + \
                                  swb.get_serial_number() + wms.get_serial_number() + wmg.get_serial_number() + \
                                  smh.get_serial_number() + smb.get_serial_number()
        self.assertIs(type(serial_numbers_sum_type), int)

    def test_initiate_with_missing_data(self):
        """Initiating object with missing data gives a TypeError"""
        with self.assertRaises(TypeError):
            ArmorDetails(cs.steel, 1.0, 70, cs.slim + " " + cs.even)


if __name__ == '__main__':
    unittest.main()
