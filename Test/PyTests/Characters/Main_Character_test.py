import random
import pytest
from src.Data_Loading.Data_Placement import DataFromLastSave
from src.Armor.Weapon import Weapon
from src.Armor.Shield import Shield
from src.Armor.Aid import Aid
from src.Characters.Main_Character import MainCharacter
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
global_weapon = (DataFromLastSave().get_armor_data())["Weapons"].search(Weapon("Wep", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh").serial_number_int())
global_shield = (DataFromLastSave().get_armor_data())["Shields"].search(Shield("Wep", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh").serial_number_int())
global_aid = Aid("Cure", cs.health, 3)


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
        MainCharacter(1200, undercover, 1, 1)


@pytest.mark.parametrize("undercover", ["True", [1], -1.0, None])
def test_change_undercover_wrong_input_data_type(undercover):
    c = MainCharacter(1200, True, 1, 1)
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
        MainCharacter(1200, True, 1, 1, item1, item2, item3, item4)


@pytest.mark.parametrize("item1, item2",
                         [(None, None),
                          (12, None),
                          ("f", True),
                          (True, True),
                          (23, 0),
                          (100, "Nothing"),
                          ])
def test_no_input_items(item1, item2):
    with pytest.raises(TypeError):
        if item1 is None:
            MainCharacter()
        elif item2 is None:
            MainCharacter(item1)
        else:
            MainCharacter(item1, item2, 1, 1)


@pytest.fixture
def example_good_character():
    """This function gives a MainCharacter data fixture."""
    return MainCharacter(100, False, 1, 1, global_aid, global_weapon, global_shield, global_aid, global_aid)


@pytest.mark.parametrize("fixture", [True, False])
def test_item_function(example_good_character, fixture):
    """Here we test if the character can return the items correctly."""
    if fixture:
        ite = example_good_character.items()
    else:
        ite = MainCharacter(1200, True, 1, 1).items()
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
    """Here we test the possibility of changing undercover to invalid value, to a valid value and if the getter works"""
    if setget:
        if type(value) == bool:
            example_good_character.undercover = value
            assert value == example_good_character.undercover
        else:
            with pytest.raises(TypeError):
                example_good_character.undercover = value


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
            assert relevant_object.serial_number() == example_good_character.weapon.serial_number()
        else:
            with pytest.raises(ValueError):
                example_good_character.weapon = relevant_object.serial_number()
    else:
        if correct:
            with pytest.raises(AttributeError):
                del example_good_character.weapon
        else:
            weapon_value = example_good_character.weapon


@pytest.mark.parametrize("tree, damage, repetitions, expected",
                         [(True, 0.1, 3, 1),
                          (True, 0.05, 1, 1),
                          (True, 0.2, 0, 1),
                          (False, 0.06, 4, 0.78074896),
                          (False, 0.35, 1, 0.65),
                          (False, 0.05, 3, 0.857375),
                          ])
def test_weapon_not_changing_in_tree(example_good_character, tree, damage, repetitions, expected):
    """
    Here we check that if the details in a weapon are changing, it will not affect the weapon in the tree.
    We also check the calculation of weapon's effectiveness.
    """
    example_good_character.weapon.renew_armor_efficiency()
    for _ in range(repetitions):
        example_good_character.weapon.armor_efficiency_update(damage)
    if tree:
        ser = example_good_character.weapon.serial_number_int()
        assert ((DataFromLastSave().get_armor_data())["Weapons"].search(ser)).armor_efficiency() == expected
    else:
        assert round(example_good_character.weapon.armor_efficiency(), 8) == expected


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


@pytest.mark.parametrize("tree, damage, repetitions, expected",
                         [(True, 0.1, 3, 1),
                          (True, 0.05, 1, 1),
                          (True, 0.2, 0, 1),
                          (False, 0.06, 4, 0.78074896),
                          (False, 0.35, 1, 0.65),
                          (False, 0.05, 3, 0.857375),
                          ])
def test_shield_not_changing_in_tree(example_good_character, tree, damage, repetitions, expected):
    """
    Here we check that if the details in a shield are changing, it will not affect the weapon in the tree.
    We also check the calculation of weapon's effectiveness.
    """
    example_good_character.shield.renew_armor_efficiency()
    for _ in range(repetitions):
        example_good_character.shield.armor_efficiency_update(damage)
    if tree:
        ser = example_good_character.shield.serial_number_int()
        assert ((DataFromLastSave().get_armor_data())["Weapons"].search(ser)).armor_efficiency() == expected
    else:
        assert round(example_good_character.shield.armor_efficiency(), 8) == expected


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


@pytest.mark.parametrize("case, move, expected",
                         [(1, (1, 1), (2, 2)),
                          (1, (-1, 1), (0, 2)),
                          (1, (0, 1), (1, 2)),
                          (1, (-1, 0), (0, 1)),
                          (2, None, 1),
                          (3, None, 1),
                          (3, (-5, 0), 1),
                          (3, (0, 1.1), 1),
                          (3, (1, 3), 1),
                          (3, [1, 1], 1),
                          (3, 1, 1),
                          (3, "Hello", 1),
                          (3, True, 1),
                          ])
def test_legal_and_illegal_moves(example_good_character, case, move, expected):
    """
    Testing the different operations with a character's position. A character moves in the right direction given
    the instruction. Illegal move is raising an error. Delete character's position is impossible.
    """
    if case == 1:
        example_good_character.position = move
        assert example_good_character.position == expected
    elif case == 2:
        with pytest.raises(AttributeError):
            del example_good_character.position
    elif case == 3:
        with pytest.raises(AssertionError):
            example_good_character.position = move


@pytest.mark.parametrize("case, move, repetitions, expected",
                         [(True, (1, 1), 5, (5, 6)),
                          (True, (-1, 1), 8, (-8, 9)),
                          (False, (0, 1), 4, (1, 2)),
                          (False, (-1, 0), 8, (0, 1)),
                          ])
def test_repetitive_moves(example_good_character, case, move, repetitions, expected):
    """
    Testing that a character can repeat a certain move, and have a combination of moves.
    Validating that in the case of a wrong input data type, an assertion error is raised.
    """
    for _ in range(repetitions):
        example_good_character.position = move
    if case:
        example_good_character.position = (-1, 0)
        assert example_good_character.position == expected
    else:
        illegal_move = random.choice([None, "Hello", (1, 3)])
        with pytest.raises(AssertionError):
            example_good_character.position = illegal_move


@pytest.mark.parametrize("legal, damage, expected",
                         [(True, 5.5, 94.5),
                          (True, 82, 18),
                          (True, 252, 0),
                          (False, [6], 0),
                          (False, "23", 1),
                          (False, None, 0),
                          (False, True, 1),
                          ])
def test_updating_legal_and_illegal_life(example_good_character, legal, damage, expected):
    """
    Testing that the updating character's life operates correctly.
    """
    if legal:
        example_good_character.life = damage
        assert expected == example_good_character.life
    else:
        with pytest.raises(TypeError):
            example_good_character.life = damage


@pytest.mark.parametrize("damage, repetitions, expected_life, expected_alive",
                         [(5.5, 20, 0, False),
                          (82, 18, 0, False),
                          (252, 1, 0, False),
                          (20, 3, 40, True),
                          (5.5, 5, 72.5, True),
                          ])
def test_repetitive_attack(example_good_character, damage, repetitions, expected_life, expected_alive):
    """
    Testing that the updating character's life operates correctly.
    """
    for _ in range(repetitions):
        example_good_character.life = damage
    assert example_good_character.life == expected_life and example_good_character.alive == expected_alive


@pytest.mark.parametrize("life", [True, False])
def test_delete_life_and_alive(example_good_character, life):
    """Verifying that the delete functions works."""
    with pytest.raises(AttributeError):
        if life:
            del example_good_character.life
        else:
            del example_good_character.alive


@pytest.mark.parametrize("resurrect", [True, False, "True", [True], None, 1])
def test_alive_setter(example_good_character, resurrect):
    """
    Testing that the updating character's alive operates correctly.
    """
    current_life = example_good_character.life
    if type(resurrect) == bool:
        if resurrect:
            example_good_character.life = 5 + current_life
            example_good_character.alive = resurrect
            assert example_good_character.life == current_life
        else:
            example_good_character.alive = resurrect
            assert example_good_character.life == 0
    else:
        with pytest.raises(TypeError):
            example_good_character.alive = resurrect


@pytest.mark.parametrize("damage, repetitions, recharge, expected",
                         [(5.5, 20, 50, 0),
                          (82, 1, 20, 38),
                          (22, 3, 500, 100),
                          (20, 3, 40, 80),
                          ])
def test_recharge_life(example_good_character, damage, repetitions, recharge, expected):
    """
    Testing that the updating character's life operates correctly.
    """
    for _ in range(repetitions):
        example_good_character.life = damage
    example_good_character.recharge_life(recharge)
    assert example_good_character.life == expected


@pytest.mark.parametrize("damage, repetitions, recharge, expected",
                         [(5.5, 20, 50, 0),
                          (82, 1, 20, 38),
                          (22, 3, 500, 100),
                          (20, 3, 40, 80),
                          (True, 3, 40, 80),
                          (None, 3, 40, 80),
                          ([20], 3, 40, 80),
                          (82, 1, None, 38),
                          (22, 3, True, 100),
                          (20, 3, [40], 80),
                          ])
def test_recharge_life(example_good_character, damage, repetitions, recharge, expected):
    """
    Testing that the recharging character's life operates correctly. Checking that recharging gives the
    correct life amount. That an error occurs when recharging with invalid value.
    """
    if type(damage) != int and type(damage) != float:
        with pytest.raises(TypeError):
            example_good_character.recharge_life(damage)
    else:
        for _ in range(repetitions):
            example_good_character.life = damage
        if type(recharge) != int and type(recharge) != float:
            with pytest.raises(TypeError):
                example_good_character.recharge_life(recharge)
        else:
            example_good_character.recharge_life(recharge)
            assert example_good_character.life == expected


@pytest.mark.parametrize("redefine_life, new_max",
                         [(True, 5.5),
                          (True, 82),
                          (True, 252),
                          (True, [6]),
                          (True, "23"),
                          (True, None),
                          (True, True),
                          (False, True),
                          ])
def test_updating_legal_and_illegal_life(example_good_character, redefine_life, new_max):
    """
    Testing that the updating character's life operates correctly.
    """
    if redefine_life:
        if type(new_max) in [int, float] and new_max > 0:
            example_good_character.full_life = new_max
            assert new_max == example_good_character.full_life
        else:
            with pytest.raises(TypeError):
                example_good_character.full_life = new_max
    else:
        with pytest.raises(AttributeError):
            del example_good_character.full_life

#Must implement everything for full_life

#Must implement symbol and aids_info methods
