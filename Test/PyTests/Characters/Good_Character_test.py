import pytest
from src.Armor.Weapon import Weapon
from src.Armor.Shield import Shield
from src.Armor.Aid import Aid
from src.Characters.Good_Character import GoodCharacter
from src.Common_general_functionalities import common_strings as cs


"""
Here we shall test the following:
    1. Attribute undercover datatype testing                                v
    2. Initializing with wrong items                                        v
    3. Does the item function returns all the items                         v
    4. Is undercover getter and setter works                                v
    5. Validating getter and setter for weapon and shield                   v
    6. Validating getter and setter for energy                              v
    7. Validating renew-energy                                              v
"""
global_weapon = Weapon("Wep", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh")
global_shield = Shield("Shi", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh")
global_aid = Aid("Cure")


class WrongClass:
    def __init__(self):
        self._name = "Meaningless"
        self._serial_number = "Meaning123"

    def name(self):
        return self._name

    def serial_number(self):
        return self._serial_number


wrong_object = WrongClass()


@pytest.mark.parametrize("undercover", ["True", [1], -1.0, None])
def test_undercover_wrong_input_data_type(undercover):
    with pytest.raises(TypeError):
        GoodCharacter(1200, undercover)


@pytest.mark.parametrize("undercover", ["True", [1], -1.0, None])
def test_change_undercover_wrong_input_data_type(undercover):
    c = GoodCharacter(1200, True)
    print(c.undercover)
    with pytest.raises(TypeError):
        c.undercover = undercover


@pytest.mark.parametrize("item1, item2, item3, item4",
                         [(global_weapon, global_weapon, global_shield, global_aid),
                          (global_weapon, global_shield, global_shield, global_aid),
                          (global_weapon, global_shield, wrong_object, global_aid),
                          (wrong_object, wrong_object, wrong_object, wrong_object),
                          (["Wrong"], ["Data Type"], 23, 3.3),
                          (None, None, None, None),
                          ])
def test_wrong_input_items(item1, item2, item3, item4):
    with pytest.raises(AttributeError):
        GoodCharacter(1200, True, item1, item2, item3, item4)


@pytest.mark.parametrize("item1, item2",
                         [(None, None),
                          (12, None),
                          ("f", True),
                          (True, True),
                          (23, 0),
                          (100, "Nothing"),
                          ])
def test_no_input_items(item1, item2):
    if item1 is None:
        with pytest.raises(TypeError):
            GoodCharacter()
    elif item2 is None:
        with pytest.raises(TypeError):
            GoodCharacter(item1)
    else:
        with pytest.raises(TypeError):
            GoodCharacter(item1, item2)


@pytest.fixture
def example_good_character():
    """This function gives a GoodCharacter data fixture."""
    return GoodCharacter(100, False, global_aid, global_weapon, global_shield, global_aid, global_aid)


@pytest.mark.parametrize("fixture", [True, False])
def test_item_function(example_good_character, fixture):
    if fixture:
        ite = example_good_character.items()
    else:
        ite = GoodCharacter(1200, True).items()
    print(ite)
    for i in ite:
        if (i[1])[:6] not in ["Weapon", "Shield"] and (i[1])[:3] != "Aid":
            raise ValueError("There is an invalid item in among the items: {!r}".format(i))


@pytest.mark.parametrize("setget, value",
                         [(False, None),
                          (True, None),
                          (True, True),
                          (True, False),
                          (True, 3),
                          (True, "True"),
                          ])
def test_undercover(example_good_character, setget, value):
    if setget:
        if type(value) == bool:
            example_good_character.undercover = value
        else:
            with pytest.raises(TypeError):
                example_good_character.undercover = value
    else:
        undercover_value = example_good_character.undercover
        print(undercover_value)


@pytest.mark.parametrize("setget, correct, relevant_object",
                         [(True, True, Weapon("Wooden Gun", 5, cs.wood_abaci, 20, cs.broad + " " + cs.even, True, "Klook")),
                          (True, True, global_weapon),
                          (True, False, Weapon("Low Wooden Gun", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom")),
                          (True, False, wrong_object),
                          (True, False, global_shield),
                          (True, False, Weapon("Excellent Sword", 3333, cs.titanium, 99.9, cs.slim + " " + cs.long, False, "Baam")),
                          (False, False, None),
                          (False, True, None),
                          ])
def test_weapon(example_good_character, setget, correct, relevant_object):
    """
    Comprehensive testing of the weapon attribute:
    1. It is possible to update character's weapon, if it exists in the data (cases 1-2).
    2. It is impossible to update character's weapon if it doesn't exist in the data, or if it is not a weapon (cases 3-6).
    3. The getter works (case 7).
    4. The anti-deleter works (case 8).
    """
    if setget:
        if correct:
            example_good_character.weapon = relevant_object.serial_number()
        else:
            with pytest.raises(ValueError):
                example_good_character.weapon = relevant_object.serial_number()
    else:
        if correct:
            with pytest.raises(AttributeError):
                del example_good_character.weapon
        else:
            weapon_value = example_good_character.weapon
            print(weapon_value)


@pytest.mark.parametrize("setget, correct, relevant_object",
                         [(True, True, Shield("Wooden Body Shield", 5, cs.wood_abaci, 20, cs.broad + " " + cs.even, True, "Klook")),
                          (True, True, global_shield),
                          (True, False, Shield("Low Wooden Body Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom")),
                          (True, False, wrong_object),
                          (True, False, global_weapon),
                          (True, False, Shield("Excellent Hand Shield", 3333, cs.titanium, 99.9, cs.slim + " " + cs.long, False, "Baam")),
                          (False, False, None),
                          (False, True, None),
                          ])
def test_shield(example_good_character, setget, correct, relevant_object):
    """
    Comprehensive testing of the shield attribute:
    1. It is possible to update character's shield, if it exists in the data (cases 1-2).
    2. It is impossible to update character's shield if it doesn't exist in the data, or if it is not a shield (cases 3-6).
    3. The getter works (case 7).
    4. The anti-deleter works (case 8).
    """
    if setget:
        if correct:
            example_good_character.shield = relevant_object.serial_number()
        else:
            with pytest.raises(ValueError):
                example_good_character.shield = relevant_object.serial_number()
    else:
        if correct:
            with pytest.raises(AttributeError):
                del example_good_character.shield
        else:
            shield_value = example_good_character.shield
            print(shield_value)


@pytest.mark.parametrize("step, repetitions, value, expected",
                         [(True, 4, 10, 92),
                          (True, 80, 5.5, 12.0),
                          (False, 3, 0, 55),
                          (False, 5, 1, 25),
                          ])
def test_energy_after_action(example_good_character, step, repetitions, value, expected):
    """
    Testing that the character's energy is correct after several changes.
    """
    for _ in range(repetitions):
        example_good_character.energy = [step, value]
    assert round(example_good_character.energy, 5) == expected


@pytest.mark.parametrize("case, step, value",
                         [(1, True, 4),
                          (2, 1, 80),
                          (3, 2, 80),
                          (2, 3, 80),
                          (3, "True", 80),
                          (3, 0, 80),
                          (3, 1, 80),
                          (3, False, "3"),
                          (3, True, [5]),
                          (3, True, global_weapon),
                          ])
def test_energy_with_illegal_action(example_good_character, case, step, value):
    """
    Testing that there's an error when updating energy with illegal attributes.
    """
    if case == 1:
        with pytest.raises(AttributeError):
            del example_good_character.energy
    elif case == 2:
        with pytest.raises(AttributeError):
            if step == 1:
                example_good_character.energy = []
            elif step == 2:
                example_good_character.energy = 5
            else:
                example_good_character.energy = [step, value, case]
    else:
        with pytest.raises(TypeError):
            example_good_character.energy = [step, value]


@pytest.mark.parametrize("step, repetitions, value",
                         [(True, 4, 10),
                          (True, 80, 5.5),
                          (False, 3, 0),
                          (False, 5, 1),
                          ])
def test_renew_energy(example_good_character, step, repetitions, value):
    """
    Testing that the character's energy is correct after several changes and then renewing/re-initiating its energy.
    """
    for _ in range(repetitions):
        example_good_character.energy = [step, value]
    example_good_character.renew_energy()
    assert round(example_good_character.energy, 5) == 100
