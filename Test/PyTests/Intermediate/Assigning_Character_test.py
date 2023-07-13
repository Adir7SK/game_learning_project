import pytest
import random
from unittest import mock
from src.Intermediate.Assigning_Characters import Assignments
from src.Intermediate.Universe_Construction import Universe
from src.Armor.Weapon_Collection import WeaponCollection
from src.Armor.Shield_Collection import ShieldCollection
from src.Common_general_functionalities import common_strings as cs
from src.Armor.Shield import Shield
from src.Armor.Weapon import Weapon
from src.Armor.Aid import Aid


b_p = (49, 19)
e_p = [(0, 1), (15, 4), (7, 2), (8, 18)]
a_p = [(28, 2), (32, 18)]
h_p = [(41, 10), (13, 15)]


@pytest.fixture
def example_tree():
    """Creating a shield data collection fixture which will be in the form of an AVL tree."""
    shield_collection = ShieldCollection("Low Wooden Body Shield", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even, True, "Boom")
    shield_collection.insert_shield("Medium Wooden Hand Shield", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even, False, "Woosh")
    shield_collection.insert_shield("Good Metal Body Shield", 1, cs.iron, 70, cs.slim + " " + cs.even, True, "Baam")
    shield_collection.insert_shield("Medium Wooden Hand Shield Heavy", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh")
    shield_collection.insert_shield("MediumMetal Hand Shield Light", 0.15, cs.iron, 50, cs.slim + " " + cs.even, False, "Shiing")
    shield_collection.insert_shield("Excellent Metal Body Shield", 0.5, cs.titanium, 99.9, cs.slim + " " + cs.short, True, "HHH")
    weapon_collection = WeaponCollection("Low Wooden Gun", 3, cs.wood_african_mahogany, 50, cs.broad + " " + cs.even,
                                         True, "Boom")
    weapon_collection.insert_weapon("Medium Wooden Sword", 1, cs.wood_african_mahogany, 20, cs.slim + " " + cs.even,
                                    False, "Woosh")
    weapon_collection.insert_weapon("Good Metal Gun", 1, cs.iron, 70, cs.slim + " " + cs.even, True, "Baam")
    weapon_collection.insert_weapon("Medium Wooden Sword Heavy", 15, cs.inconel, 10, cs.broad + " " + cs.even, False,
                                    "Woooh")
    weapon_collection.insert_weapon("MediumMetal Sword Light", 0.15, cs.iron, 50, cs.slim + " " + cs.even, False,
                                    "Shiing")
    weapon_collection.insert_weapon("Excellent Metal Gun", 0.5, cs.titanium, 99.9, cs.slim + " " + cs.short, True,
                                    "HHH")
    tree = {cs.weapons: weapon_collection, cs.shields: shield_collection}
    return tree


@pytest.fixture
def example_universe():
    return Universe(20, 50, "earth", 3)


@pytest.fixture
def mock_universe():
    def temp1(x):
        return b_p, e_p, a_p, h_p

    @property
    def temp2(x):
        f = [[cs.no_path] * 20] * 50
        for p in e_p:
            f[p[0]][p[1]] = random.choice([cs.regular_enemy, cs.unknown])
        for p in a_p:
            f[p[0]][p[1]] = random.choice([cs.aid, cs.unknown])
        for p in h_p:
            f[p[0]][p[1]] = random.choice([cs.helper_character, cs.unknown])
        return f
    with mock.patch.multiple('src.Intermediate.Universe_Construction.Universe', boss_enemies_aid_help_charter_position=temp1, field=temp2) as mocks:
        yield mocks


@pytest.mark.parametrize("level, last_round_weakest_armor, last_round_strongest_armor",
                         [(3, (0, 0), (0, 0)),
                          (3, (400, 400), (600, 600)),
                          (3, (500, 500), (3000, 3000)),
                          ])
def test_correct_initiation(mock_universe, example_universe, example_tree, level,
                            last_round_weakest_armor, last_round_strongest_armor):
    """Verifying all the types and broad details of the enemies and aids correctly created."""
    a = Assignments(example_universe, level, example_tree, last_round_weakest_armor=last_round_weakest_armor,
                    last_round_strongest_armor=last_round_strongest_armor)
    enemies_positions, aid_positions, helper_positions = e_p, a_p, h_p
    for pos in enemies_positions:
        enem = a.get_enemy(pos)
        assert enem.alive
        assert type(enem.life) == int and enem.life > 0
        assert isinstance(enem.shield, Shield)
        assert isinstance(enem.weapon, Weapon)
        if enem.undercover:
            assert enem.symbol == cs.unknown
        else:
            assert enem.symbol == cs.regular_enemy
    for pos in helper_positions:
        enem = a.get_helper_char(pos)
        assert enem.alive
        assert type(enem.life) == int and enem.life > 0
        assert isinstance(enem.shield, Shield)
        assert isinstance(enem.weapon, Weapon)
        if enem.undercover:
            assert enem.symbol == cs.unknown
        else:
            assert enem.symbol == cs.regular_enemy
    enem = a.boss
    assert enem.alive
    assert type(enem.life) == float and enem.life > 0
    assert isinstance(enem.shield, Shield)
    assert isinstance(enem.weapon, Weapon)
    assert not enem.undercover
    assert enem.symbol == cs.boss

    for pos in aid_positions:
        assert isinstance(a.get_aid(pos), Aid)


@pytest.mark.parametrize("enemies_positions, aid_positions, level, last_round_weakest_armor, "
                         "last_round_strongest_armor",
                         [([(0, 1), (5, [4]), (7, 2), (8, 8)], [(2, 2), (3, 8)], 3, (0, 0), (0, 0)),
                          ([(0, 1), (5, 4), ("7", 2), (8, 8)], [(2, 2), (3, 8)], 3, (400, 400), (600, 600)),
                          (((0, 1), (5, 4), (7, 2), (8, 8)), [(2, 2), (3, 8)], 3, (500, 500), (3000, 3000)),
                          ([(0, 1), (5, 4), (7, 2), (8, 8)], (2, 2), 3, (500, 500), (3000, 3000)),
                          ([(0, 1), (5, 4), (7, 2), (8, 8, 5)], [(2, 2), (3, 8)], 3, (500, 500), (3000, 3000)),
                          ([(0, 1), (5, 4), (7, 2), (8, 8)], [(2), (3, 8)], 3, (500, 500), (3000, 3000)),
                          ([(0, 1), (5, 4), (7, 2), (8, 8)], [[2, 2], (3, 8)], 3, (500, 500), (3000, 3000)),
                          ([(0, 1), (5, 4), (7, 2), (8, 8)], [2, (3, 8)], 3, (500, 500), (3000, 3000)),
                          ([(0, 1), (5, 4), (7, 2), (8, 8)], [(2, 2), (3, 8)], "3", (500, 500), (3000, 3000)),
                          ([(0, 1), (5, 4), (7, 2), (8, 8)], [(2, 2), (3, 8)], 3, ("500", 500), (3000, 3000)),
                          ([(0, 1), (5, 4), (7, 2), (8, 8)], [(2, 2), (3, 8)], 3, (500, 500), ([3000], 3000)),
                          ([(0, 1), (5, 4), (7, 2), (8, 8)], [(2, 2), (3, 8)], 3, (500, 500), (3000, 3000, 2)),
                          ([(0, 1), (5, 4), (7, 2), (8, 8)], [(2, 2), (3, 8)], [3], (500, 500), (3000, 3000)),
                          ])
def test_error_in_wrong_initiation(example_tree, enemies_positions, aid_positions, level, last_round_weakest_armor,
                                   last_round_strongest_armor):
    """We get an error once we initiate with the wrong input details."""
    with pytest.raises(ValueError):
        a = Assignments(enemies_positions, aid_positions, level, example_tree,
                        last_round_weakest_armor=last_round_weakest_armor,
                        last_round_strongest_armor=last_round_strongest_armor)


@pytest.mark.parametrize("exist, pos",
                         [(True, [(5, 4), (7, 2), (8, 8), (0, 1)]),
                          (False, [(2, 2), (7, 2), (8, 8)]),
                          (False, [(0, "1"), (7, 2), (8, 8)]),
                          (False, [(7, True)]),
                          ])
def test_get_enemy(example_tree, exist, pos):
    """Verifying all the types and broad details of the enemies and aids correctly created."""
    a = Assignments([(0, 1), (5, 4), (7, 2), (8, 8)], [(2, 2), (3, 8)], 3, example_tree,
                    last_round_weakest_armor=(0, 0),
                    last_round_strongest_armor=(0, 0))
    if exist:
        assert all([a.get_enemy(p) for p in pos])
    else:
        assert not all([a.get_enemy(p) for p in pos])


@pytest.mark.parametrize("exist, pos",
                         [(True, [(2, 2), (3, 8)]),
                          (False, [(2, 2), (7, 2)]),
                          (False, [(2, "2"), (3, 8)]),
                          (False, [(2, True)]),
                          ])
def test_get_aid(example_tree, exist, pos):
    """Verifying all the types and broad details of the enemies and aids correctly created."""
    a = Assignments([(0, 1), (5, 4), (7, 2), (8, 8)], [(2, 2), (3, 8)], 3, example_tree,
                    last_round_weakest_armor=(0, 0),
                    last_round_strongest_armor=(0, 0))
    if exist:
        assert all([a.get_aid(p) for p in pos])
    else:
        assert not all([a.get_aid(p) for p in pos])


@pytest.mark.parametrize("exist, pos",
                         [(True, [(5, 4), (7, 2), (8, 8), (0, 1)]),
                          (True, [(5, 4), (8, 8), (0, 1)]),
                          (False, [(2, 2), (7, 2), (8, 8)]),
                          (False, [(0, "1"), (7, 2), (8, 8)]),
                          (False, [(7, True)]),
                          ])
def test_remove_enemy(example_tree, exist, pos):
    """Verifying all the types and broad details of the enemies and aids correctly created."""
    e_pos = [(0, 1), (5, 4), (7, 2), (8, 8)]
    a = Assignments(e_pos, [(2, 2), (3, 8)], 3, example_tree,
                    last_round_weakest_armor=(0, 0),
                    last_round_strongest_armor=(0, 0))
    e_pos = [p for p in e_pos if p not in pos]
    if exist:
        for p in pos:
            a.remove_enemy(p)
        assert not all([a.get_enemy(p) for p in pos])
        assert all([a.get_enemy(p) for p in e_pos])
    else:
        with pytest.raises(ValueError):
            for p in pos:
                a.remove_enemy(p)


@pytest.mark.parametrize("exist, pos",
                         [(True, [(2, 2)]),
                          (True, [(2, 2), (3, 8)]),
                          (False, [(2, 2), (7, 2)]),
                          (False, [(2, "2"), (3, 8)]),
                          (False, [(2, True)]),
                          ])
def test_remove_aid(example_tree, exist, pos):
    """Verifying all the types and broad details of the enemies and aids correctly created."""
    a_pos = [(2, 2), (3, 8)]
    a = Assignments([(0, 1), (5, 4), (7, 2), (8, 8)], a_pos, 3, example_tree,
                    last_round_weakest_armor=(0, 0),
                    last_round_strongest_armor=(0, 0))
    a_pos = [p for p in a_pos if p not in pos]
    if exist:
        for p in pos:
            a.remove_aid(p)
        assert not all([a.get_aid(p) for p in pos])
        assert all([a.get_aid(p) for p in a_pos])
    else:
        with pytest.raises(ValueError):
            for p in pos:
                a.remove_aid(p)
