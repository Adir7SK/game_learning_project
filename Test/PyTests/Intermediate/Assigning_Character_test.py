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
e_p = [(0, 1), (15, 4), (7, 12), (8, 18)]
a_p = [(28, 2), (32, 18)]
h_p = [(41, 10), (13, 15)]
w_p = [(21, 19), (3, 5)]
s_p = [(2, 19), (46, 0)]


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
        return b_p, e_p, a_p, h_p, w_p+s_p

    @property
    def temp2(x):
        f = [[cs.no_path] * 20] * 50
        for p in e_p:
            f[p[0]][p[1]] = random.choice([cs.regular_enemy, cs.unknown])
        for p in a_p+w_p+s_p:
            f[p[0]][p[1]] = random.choice([cs.aid, cs.unknown])
        for p in h_p:
            f[p[0]][p[1]] = random.choice([cs.helper_character, cs.unknown])
        return f
    with mock.patch.multiple('src.Intermediate.Universe_Construction.Universe',
                             boss_enemies_aid_help_charter_armor_position=temp1, field=temp2) as mocks:
        yield mocks


@pytest.mark.parametrize("last_round_weakest_armor, last_round_strongest_armor",
                         [((0, 0), (0, 0)),
                          ((400, 400), (600, 600)),
                          ((500, 500), (3000, 3000)),
                          ])
def test_correct_initiation(mock_universe, example_universe, example_tree,
                            last_round_weakest_armor, last_round_strongest_armor):
    """Verifying all the types and broad details of the enemies and aids correctly created."""
    a = Assignments(example_universe, 3, example_tree, last_round_weakest_armor=last_round_weakest_armor,
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
        help = a.get_helper_char(pos)
        assert help.alive
        assert type(help.life) == int and help.life > 0
        assert isinstance(help.shield, Shield)
        assert isinstance(help.weapon, Weapon)
        if help.undercover:
            assert help.symbol == cs.unknown
        else:
            assert help.symbol == cs.helper_character
    enem = a.boss
    assert enem.alive
    assert type(enem.life) == float and enem.life > 0
    assert isinstance(enem.shield, Shield)
    assert isinstance(enem.weapon, Weapon)
    assert not enem.undercover
    assert enem.symbol == cs.boss

    for pos in aid_positions:
        assert isinstance(a.get_aid(pos), Aid)

    for pos in w_p:
        assert isinstance(a.get_armor(pos), Weapon)

    for pos in s_p:
        assert isinstance(a.get_armor(pos), Shield)


@pytest.mark.parametrize("use_uni, level, last_round_weakest_armor, "
                         "last_round_strongest_armor",
                         [(True, "3", (500, 500), (3000, 3000)),
                          (True, 3, ("500", 500), (3000, 3000)),
                          (True, 3, (500, 500), ([3000], 3000)),
                          (True, 3, (500, 500), (3000, 3000, 2)),
                          (True, [3], (500, 500), (3000, 3000)),
                          (True, 3, (500, 500), [3000]),
                          (True, 3, 500, (3000, 4000)),
                          (False, 3, (500, 500), (3000, 3000)),
                          ])
def test_error_in_wrong_initiation(mock_universe, example_universe, example_tree, use_uni, level,
                                   last_round_weakest_armor, last_round_strongest_armor):
    """We get an error once we initiate with the wrong input details."""
    with pytest.raises(TypeError):
        a = Assignments(example_universe, level, example_tree, last_round_weakest_armor=last_round_weakest_armor,
                        last_round_strongest_armor=last_round_strongest_armor) if use_uni else Assignments(
            "Wrong_Universe_type", 3, example_tree, last_round_weakest_armor=last_round_weakest_armor,
            last_round_strongest_armor=last_round_strongest_armor)


@pytest.mark.parametrize("exist, pos",
                         [(True, e_p),
                          (False, [(2, 2), (7, 2), (8, 8)]),
                          (False, [(0, "1"), (7, 2), (8, 8)]),
                          (False, [(7, True)]),
                          ])
def test_get_enemy(mock_universe, example_universe, example_tree, exist, pos):
    """Correct enemy positions are found and incorrect positions are not."""
    a = Assignments(example_universe, 1, example_tree, last_round_weakest_armor=(0, 0),
                    last_round_strongest_armor=(0, 0))
    if exist:
        assert all([a.get_enemy(p) for p in pos])
    else:
        assert not any([a.get_enemy(p) for p in pos])


@pytest.mark.parametrize("exist, pos",
                         [(True, h_p),
                          (False, [(2, 2), (7, 2), (8, 8)]),
                          (False, [(41, "10"), (7, 2), (8, 8)]),
                          (False, [(7, True)]),
                          ])
def test_get_helper(mock_universe, example_universe, example_tree, exist, pos):
    """Correct helper character positions are found and incorrect positions are not."""
    a = Assignments(example_universe, 1, example_tree, last_round_weakest_armor=(0, 0),
                    last_round_strongest_armor=(0, 0))
    if exist:
        assert all([a.get_helper_char(p) for p in pos])
    else:
        assert not any([a.get_helper_char(p) for p in pos])


@pytest.mark.parametrize("exist, pos",
                         [(True, a_p),
                          (False, [(2, 2), (7, 2)]),
                          (False, [(2, "2"), (3, 8)]),
                          (False, [(2, True)]),
                          ])
def test_get_aid(mock_universe, example_universe, example_tree, exist, pos):
    """Verifying all the types and broad details of the enemies and aids correctly created."""
    a = Assignments(example_universe, 1, example_tree, last_round_weakest_armor=(0, 0),
                    last_round_strongest_armor=(0, 0))
    if exist:
        assert all([a.get_aid(p) for p in pos])
    else:
        assert not any([a.get_aid(p) for p in pos])


@pytest.mark.parametrize("exist, pos",
                         [(True, w_p+s_p),
                          (False, [(2, 2), (7, 2)]),
                          (False, [(2, "2"), (3, 8)]),
                          (False, [(2, True)]),
                          ])
def test_get_armor(mock_universe, example_universe, example_tree, exist, pos):
    """Verifying all the types and broad details of the enemies and aids correctly created."""
    a = Assignments(example_universe, 1, example_tree, last_round_weakest_armor=(0, 0),
                    last_round_strongest_armor=(3000, 3500))
    if exist:
        assert all([a.get_armor(p) for p in pos])
    else:
        assert not any([a.get_armor(p) for p in pos])


@pytest.mark.parametrize("exist, pos",
                         [(True, e_p),
                          (True, e_p[1:]),
                          (False, [(2, 2), (7, 2), (8, 8)]),
                          (False, [(0, "1"), (7, 2), (8, 8)]),
                          (False, [(7, True)]),
                          ])
def test_remove_enemy(mock_universe, example_universe, example_tree, exist, pos):
    """Verifying all the types and broad details of the enemies and aids correctly created."""
    a = Assignments(example_universe, 4, example_tree, last_round_weakest_armor=(0, 0),
                    last_round_strongest_armor=(3000, 3500))
    e_pos = [p for p in e_p if p not in pos]
    if exist:
        for p in pos:
            a.remove_enemy(p)
        assert not all([a.get_enemy(p) for p in pos])
        assert all([a.get_enemy(p) for p in e_pos])
    else:
        for p in pos:
            with pytest.raises(ValueError):
                a.remove_enemy(p)


@pytest.mark.parametrize("exist, pos",
                         [(True, h_p),
                          (True, [h_p[1]]),
                          (False, e_p),
                          (False, [(2, 2), (7, 2), (8, 8)]),
                          (False, [(0, "1"), (7, 2), (8, 8)]),
                          (False, [(7, True)]),
                          ])
def test_remove_helper(mock_universe, example_universe, example_tree, exist, pos):
    """Verifying all the types and broad details of the enemies and aids correctly created."""
    a = Assignments(example_universe, 4, example_tree, last_round_weakest_armor=(0, 0),
                    last_round_strongest_armor=(3000, 3500))
    h_pos = [p for p in h_p if p not in pos]
    if exist:
        for p in pos:
            a.remove_helper_char(p)
        assert not all([a.get_helper_char(p) for p in pos])
        assert all([a.get_helper_char(p) for p in h_pos])
    else:
        for p in pos:
            with pytest.raises(ValueError):
                a.remove_helper_char(p)


@pytest.mark.parametrize("exist, pos",
                         [(True, a_p),
                          (True, [a_p[1]]),
                          (False, w_p),
                          (False, [(2, 2), (7, 2), (8, 8)]),
                          (False, [(0, "1"), (7, 2), (8, 8)]),
                          (False, [(7, True)]),
                          ])
def test_remove_aid(mock_universe, example_universe, example_tree, exist, pos):
    """Verifying all the types and broad details of the aid and aids correctly created."""
    a = Assignments(example_universe, 4, example_tree, last_round_weakest_armor=(2000, 1500),
                    last_round_strongest_armor=(2500, 3000))
    a_pos = [p for p in a_p if p not in pos]
    if exist:
        for p in pos:
            a.remove_aid(p)
        assert not all([a.get_aid(p) for p in pos])
        assert all([a.get_aid(p) for p in a_pos])
    else:
        for p in pos:
            with pytest.raises(ValueError):
                a.remove_aid(p)


@pytest.mark.parametrize("exist, pos",
                         [(True, w_p+s_p),
                          (True, [w_p[1]]),
                          (True, [s_p[0]]),
                          (False, a_p),
                          (False, [(2, 2), (7, 2), (8, 8)]),
                          (False, [(0, "1"), (7, 2), (8, 8)]),
                          (False, [(7, True)]),
                          ])
def test_remove_armor(mock_universe, example_universe, example_tree, exist, pos):
    """Verifying all the types and broad details of the aid and aids correctly created."""
    a = Assignments(example_universe, 4, example_tree, last_round_weakest_armor=(2000, 1500),
                    last_round_strongest_armor=(2500, 3000))
    a_pos = [p for p in w_p+s_p if p not in pos]
    if exist:
        for p in pos:
            a.remove_armor(p)
        assert not all([a.get_armor(p) for p in pos])
        assert all([a.get_armor(p) for p in a_pos])
    else:
        for p in pos:
            with pytest.raises(ValueError):
                a.remove_armor(p)
