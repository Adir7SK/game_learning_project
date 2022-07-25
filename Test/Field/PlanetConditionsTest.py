import unittest
from src.Field.PlanetConditions import planets


class PlanetTest(unittest.TestCase):
    """
    Here we test the following: 
    Do we get an error when inserting invalid values
    Validating that changing an attribute of one instance will not effect another instance
    Is the gravity calculation correct
    Do we get an error when trying to delete a value
    Can we change an attribute to a valid value
    """
    pluto = planets["pluto"]
    venus = planets["venus"]
    
    def test_negative_mass_error(self, planet=pluto):
        """Are we getting ValueError when setting an unrealistic value"""
        with self.assertRaises(ValueError):
            planet.mass = -1

    def test_negative_radius_error(self, planet=venus):
        """Are we getting ValueError when setting an unrealistic value"""
        with self.assertRaises(ValueError):
            planet.radius = 0

    def test_changing_value_of_one_not_effecting_other(self, planet1=pluto, planet2=venus):
        """Checking that changing the mass value of one planet will not effect the other"""
        planet1.mass = 50
        self.assertNotEqual(50, planet2.mass)

    def test_currect_gravity_value_venus(self, planet=venus):
        """Checking whether the gravity calculation is correct"""
        self.assertEqual(8.86, planet.gravitational_force)

    def test_currect_gravity_value_pluto(self, planet=pluto):
        """Checking whether the gravity calculation is correct"""
        self.assertEqual(0.62, planet.gravitational_force)

    def test_delete(self, planet=pluto):
        """Will we get an error when trying to delete a value"""
        with self.assertRaises(AttributeError):
            del planet.mass

    def test_possible_to_change_allowed_value(self, planet=venus):
        """Changing attribute to a valid value"""
        planet.radius = 100
        self.assertEqual(100, planet.radius)


if __name__ == '__main__':
    unittest.main()
