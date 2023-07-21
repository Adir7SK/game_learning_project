import pytest
import random
from unittest import mock
from src.Intermediate.Universe_Construction import Universe
from src.Final.Fight_Handle import Fight
from src.Common_general_functionalities import common_strings as cs
from src.Data_Loading.Data_Placement import DataFromLastSave
from src.Characters.Good_Character import GoodCharacter
from src.Characters.Main_Character import MainCharacter
from src.Characters.Bad_Character import BadCharacter
from src.Armor.Shield import Shield
from src.Armor.Weapon import Weapon
from src.Armor.Aid import Aid

"""
Tests to do:
1. Correct initialization.                          v
2. Incorrect initialization.                        v
3. Result after n times using player_is_hitting
4. Result after n times using enemy_is_hitting
5. Check fight_ongoing.
6. Check update_players.
"""
global_weapon = (DataFromLastSave().get_armor_data())[cs.weapons].search(Weapon("Wep", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh").serial_number_int())
global_shield = (DataFromLastSave().get_armor_data())[cs.shields].search(Shield("Wep", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh").serial_number_int())
global_aid = Aid("Cure", cs.health, 3)
w_strength = global_weapon.strength()
w_speed = global_weapon.speed()
s_strength = global_shield.strength()
s_speed = global_shield.speed()
cond = w_speed >= s_speed


@pytest.fixture
def example_good_character():
    """This function gives a GoodCharacter data fixture."""
    return GoodCharacter(100, False, global_weapon, global_shield)


@pytest.fixture
def example_main_character():
    """This function gives a MainCharacter data fixture."""
    return MainCharacter(100, global_aid, global_weapon, global_shield, global_aid, global_aid)


@pytest.fixture
def example_bad_character():
    """This function gives a GoodCharacter data fixture."""
    return BadCharacter(50, False, global_weapon, global_shield)


def test_correct_initiation(example_main_character, example_good_character, example_bad_character):
    """Verifying all the types and broad details of the enemies, aids, and boss correctly created."""
    f = Fight(example_main_character, example_bad_character, False, example_good_character, example_good_character)
    assert f.fight_ongoing()
    assert f.main_character == example_main_character
    assert f.enemy == example_bad_character
    assert len(f.additional_good_characters) == 2


@pytest.mark.parametrize("attribute, test_case",
                         [("main", True),
                          ("main", False),
                          ("enemy", True),
                          ("enemy", False),
                          ("print_sound", True),
                          ("print_sound", False),
                          ("additional", True),
                          ("additional", False),
                          ("add-dead", False),
                          ("main-dead", False),
                          ("bad-dead", False),
                          ])
def test_incorrect_initiation(example_main_character, example_good_character, example_bad_character, attribute, test_case):
    if attribute == "main":
        with pytest.raises(AttributeError):
            if test_case:
                Fight(example_bad_character, example_bad_character, False, example_good_character,
                      example_good_character)
            else:
                Fight(5, example_bad_character, False, example_good_character, example_good_character)
        return
    elif attribute == "enemy":
        with pytest.raises(AttributeError):
            if test_case:
                Fight(example_main_character, example_good_character, False, example_good_character,
                      example_good_character)
            else:
                Fight(example_main_character, "Wrong input", False, example_good_character, example_good_character)
        return
    elif attribute == "print_sound":
        with pytest.raises(TypeError):
            if test_case:
                Fight(example_main_character, example_bad_character, example_bad_character, example_good_character,
                      example_good_character)
            else:
                Fight(example_main_character, example_bad_character, 1, example_good_character, example_good_character)
        return
    elif attribute == "additional":
        with pytest.raises(AttributeError):
            if test_case:
                Fight(example_main_character, example_bad_character, False, example_bad_character,
                      example_good_character)
            else:
                Fight(example_main_character, example_bad_character, False, "Wrong type", example_good_character)
        return
    else:
        with pytest.raises(AttributeError):
            if attribute == "add-dead":
                a_c = GoodCharacter(100, False, global_weapon, global_shield)
                a_c.alive = False
                Fight(example_main_character, example_bad_character, False, a_c, example_good_character)
            elif attribute == "main-dead":
                a_c = MainCharacter(100, global_aid, global_weapon, global_shield, global_aid, global_aid)
                a_c.alive = False
                Fight(a_c, example_bad_character, False, example_good_character)
            elif attribute == "bad-dead":
                a_c = BadCharacter(100, False, global_weapon, global_shield)
                a_c.alive = False
                Fight(example_main_character, a_c, False, example_good_character)
        return


@pytest.mark.parametrize("rep, n_helper, result",
                         [(2, 2, max(0, 50-3*(w_strength if cond else w_strength-s_strength))),
                          (1, 200, 0),
                          (2, 0, max(0, 50-2*(w_strength if cond else w_strength-s_strength))),
                          ])
def test_player_is_hitting(example_main_character, example_good_character, example_bad_character, rep, n_helper, result):
    h_charac_list = [example_good_character]*n_helper
    f = Fight(example_main_character, example_bad_character, False, *h_charac_list)
    for _ in range(rep):
        result -= f.main_character.strength
        f.player_is_hitting()
    result = max(0, result)
    assert f.main_character.life == 100
    assert f.enemy.life == result
    if f.enemy.life:
        assert f.enemy.alive
    else:
        assert not f.enemy.alive


@pytest.mark.parametrize("rep, n_helper, result",
                         [(2, 2, max(0, 50-3*(w_strength if cond else w_strength-s_strength))),
                          (1, 200, 0),
                          (2, 0, max(0, 50-2*(w_strength if cond else w_strength-s_strength))),
                          ])
def test_enemy_is_hitting(example_main_character, example_good_character, example_bad_character, rep, n_helper, result):
    h_charac_list = [example_good_character]*n_helper
    f = Fight(example_main_character, example_bad_character, False, *h_charac_list)
    for _ in range(rep):
        result -= f.main_character.strength
        f.player_is_hitting()
    result = max(0, result)
    assert f.main_character.life == 100
    assert f.enemy.life == result
    if f.enemy.life:
        assert f.enemy.alive
    else:
        assert not f.enemy.alive

"""
The last function is not done at all - also use update_players method, to give more life to the main character, so he'll
survive after the other helper characters died. 
We have to check that dead good characters (or any dead characters) do not continue to exist.
"""