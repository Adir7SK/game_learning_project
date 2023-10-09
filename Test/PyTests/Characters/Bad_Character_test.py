import pytest
from src.Data_Loading.Data_Placement import GameDetailsData
from src.Armor.Weapon import Weapon
from src.Armor.Shield import Shield
from src.Armor.Aid import Aid
from src.Characters.Bad_Character import BadCharacter
from src.Common_general_functionalities import common_strings as cs


"""
Here we shall test the following:
    1. Attribute undercover datatype testing                                v
    2. Initializing with wrong items                                        v
    3. Is undercover getter and setter works                                v
    4. Validating getter and setter for weapon and shield                   v
"""
global_weapon = GameDetailsData().load_weapons().weapon_collection.right.obj
global_shield = GameDetailsData().load_shields().shield_collection.right.obj
global_aid = Aid("Cure", cs.health, 3)


@pytest.mark.parametrize("undercover", ["True", [1], -1.0, None])
def test_undercover_wrong_input_data_type(undercover):
    with pytest.raises(TypeError):
        BadCharacter(1200, undercover)


@pytest.mark.parametrize("undercover", ["True", [1], -1.0, None])
def test_change_undercover_wrong_input_data_type(undercover):
    c = BadCharacter(1200, True)
    print(c.undercover)
    with pytest.raises(TypeError):
        c.undercover = undercover


@pytest.mark.parametrize("item1, item2, item3",
                         [(global_weapon, global_weapon, global_shield),
                          (global_weapon, global_shield, global_shield),
                          (global_weapon, global_shield, global_aid),
                          (global_aid, global_aid, global_aid),
                          (["Wrong"], ["Data Type"], 23.3),
                          (None, None, None),
                          ])
def test_too_many_input_items(item1, item2, item3):
    with pytest.raises(AttributeError):
        BadCharacter(1200, True, item1, item2, item3)


@pytest.mark.parametrize("item1, item2",
                         [(None, None),
                          (12, None),
                          ("f", True),
                          (True, True),
                          (23, 0),
                          (100, "Nothing"),
                          ])
def test_wrong_type_input_items(item1, item2):
    with pytest.raises(TypeError):
        if item1 is None:
            BadCharacter()
        elif item2 is None:
            BadCharacter(item1)
        else:
            BadCharacter(item1, item2)


@pytest.fixture
def example_bad_character():
    """This function gives a BadCharacter data fixture."""
    return BadCharacter(100, False, global_weapon, global_shield)


@pytest.mark.parametrize("fixture", [True, False])
def test_item_function(example_bad_character, fixture):
    if fixture:
        ite = example_bad_character.items()
    else:
        ite = BadCharacter(1200, True).items()
    assert ite is None


@pytest.mark.parametrize("setget, value",
                         [(False, None),
                          (True, None),
                          (True, True),
                          (True, False),
                          (True, 3),
                          (True, "True"),
                          ])
def test_undercover(example_bad_character, setget, value):
    if setget:
        if type(value) == bool:
            example_bad_character.undercover = value
        else:
            with pytest.raises(TypeError):
                example_bad_character.undercover = value
    else:
        undercover_value = example_bad_character.undercover
        print(undercover_value)


@pytest.mark.parametrize("setget, correct, relevant_object",
                         [(True, True, GameDetailsData().load_weapons().weapon_collection.left.obj),
                          (True, True, GameDetailsData().load_weapons().weapon_collection.obj),
                          (True, False, Weapon("Low Wooden Gun", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom")),
                          (True, False, global_aid),
                          (True, False, global_shield),
                          (True, False, Weapon("Excellent Sword", 3333, cs.titanium, 99.9, cs.slim + " " + cs.long, False, "Baam")),
                          (False, False, None),
                          (False, True, None),
                          ])
def test_weapon(example_bad_character, setget, correct, relevant_object):
    """
    Comprehensive testing of the weapon attribute:
    1. It is possible to update character's weapon, if it exists in the data (cases 1-2).
    2. It is impossible to update character's weapon if it doesn't exist in the data, or if it is not a weapon (cases 3-6).
    3. The getter works (case 7).
    4. The anti-deleter works (case 8).
    """
    if setget:
        if correct:
            example_bad_character.weapon = relevant_object.serial_number()
        else:
            with pytest.raises(ValueError):
                example_bad_character.weapon = relevant_object.serial_number()
    else:
        if correct:
            with pytest.raises(AttributeError):
                del example_bad_character.weapon
        else:
            weapon_value = example_bad_character.weapon
            print(weapon_value)


@pytest.mark.parametrize("setget, correct, relevant_object",
                         [(True, True, GameDetailsData().load_shields().shield_collection.left.obj),
                          (True, True, GameDetailsData().load_shields().shield_collection.obj),
                          (True, False, Shield("Low Wooden Body Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom")),
                          (True, False, global_aid),
                          (True, False, global_weapon),
                          (True, False, Shield("Excellent Hand Shield", 3333, cs.titanium, 99.9, cs.slim + " " + cs.long, False, "Baam")),
                          (False, False, None),
                          (False, True, None),
                          ])
def test_shield(example_bad_character, setget, correct, relevant_object):
    """
    Comprehensive testing of the shield attribute:
    1. It is possible to update character's shield, if it exists in the data (cases 1-2).
    2. It is impossible to update character's shield if it doesn't exist in the data, or if it is not a shield (cases 3-6).
    3. The getter works (case 7).
    4. The anti-deleter works (case 8).
    """
    if setget:
        if correct:
            example_bad_character.shield = relevant_object.serial_number()
        else:
            with pytest.raises(ValueError):
                example_bad_character.shield = relevant_object.serial_number()
    else:
        if correct:
            with pytest.raises(AttributeError):
                del example_bad_character.shield
        else:
            shield_value = example_bad_character.shield
            print(shield_value)


@pytest.mark.parametrize("legal, damage, expected",
                         [(True, 5.5, 94.5),
                          (True, 82, 18),
                          (True, 252, 0),
                          (False, [6], 0),
                          (False, "23", 1),
                          (False, None, 0),
                          (False, True, 1),
                          ])
def test_updating_legal_and_illegal_life(example_bad_character, legal, damage, expected):
    """
    Testing that the updating character's life operates correctly.
    """
    if legal:
        example_bad_character.life = damage
        assert expected == example_bad_character.life
    else:
        with pytest.raises(TypeError):
            example_bad_character.life = damage


@pytest.mark.parametrize("damage, repetitions, expected_life, expected_alive",
                         [(5.5, 20, 0, False),
                          (82, 18, 0, False),
                          (252, 1, 0, False),
                          (20, 3, 40, True),
                          (5.5, 5, 72.5, True),
                          ])
def test_repetitive_attack(example_bad_character, damage, repetitions, expected_life, expected_alive):
    """
    Testing that the updating character's life operates correctly.
    """
    for _ in range(repetitions):
        example_bad_character.life = damage
    assert example_bad_character.life == expected_life and example_bad_character.alive == expected_alive


@pytest.mark.parametrize("life", [True, False])
def test_delete_life_and_alive(example_bad_character, life):
    """Verifying that the delete functions works."""
    with pytest.raises(AttributeError):
        if life:
            del example_bad_character.life
        else:
            del example_bad_character.alive


@pytest.mark.parametrize("resurrect", [True, False, "True", [True], None, 1])
def test_alive_setter(example_bad_character, resurrect):
    """
    Testing that the updating character's alive operates correctly.
    """
    current_life = example_bad_character.life
    if type(resurrect) == bool:
        if resurrect:
            example_bad_character.life = 5 + current_life
            example_bad_character.alive = resurrect
            assert example_bad_character.life == current_life
        else:
            example_bad_character.alive = resurrect
            assert example_bad_character.life == 0
    else:
        with pytest.raises(TypeError):
            example_bad_character.alive = resurrect
