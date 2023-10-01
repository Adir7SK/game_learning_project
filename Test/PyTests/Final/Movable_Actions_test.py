import random
import pytest
from unittest import mock
from src.Final.Fight_Handle import Fight
from src.Armor.Shield_Collection import ShieldCollection
from src.Armor.Weapon_Collection import WeaponCollection
from src.Common_general_functionalities import common_strings as cs
from src.Data_Loading.Data_Placement import DataFromLastSave
from src.Characters.Good_Character import GoodCharacter
from src.Characters.Main_Character import MainCharacter
from src.Characters.Bad_Character import BadCharacter
from src.Intermediate.Assigning_Characters import Assignments
from src.Armor.Shield import Shield
from src.Armor.Weapon import Weapon
from src.Armor.Aid import Aid
from src.Final.Movable_Actions import Move
from src.Intermediate.Universe_Construction import Universe

"""
Test: correct and incorrect = c/i
1. C/I initialization.
2. step method (Many tests!!) include get info (c/i), normal step (c/i), multiple step (c/i), use aid (c/i),
                                    go to fight (c/i), move after fight (c/i)
3. _fight_update method that it handles a fight correctly (try to create a very strong main_character vs weak enemy and
                                                            vice versa).

        * Must mock: creating a field (since we want to go into a fight), player_is_hitting, enemy_is_hitting,
                    fight_ongoing
        * Fake inputs: main_character, good_character, Orc, field
"""
global_weapon = (DataFromLastSave().get_armor_data())[cs.weapons].search(Weapon("Wep", 15, cs.inconel, 10, cs.broad + " " + cs.even, False, "Woooh").serial_number_int())
global_shield = (DataFromLastSave().get_armor_data())[cs.shields].search(Shield("Shi", 15, cs.wood_abaci, 10, cs.broad + " " + cs.not_even, False, "Woooh").serial_number_int())
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


b_p = (49, 19)                                  # Boss position
e_p = [(0, 1), (15, 4), (7, 12), (8, 18)]       # Enemies position
a_p = [(28, 2), (32, 18)]                       # Aid position
h_p = [(41, 10), (13, 15)]                      # Helper characters position
w_p = [(21, 19), (3, 5)]                        # Weapon positions
s_p = [(2, 19), (46, 0)]                        # Shield positions
v_p = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]  # Path


@pytest.fixture
def example_tree():
    """Creating an armor data collection fixture which will be in the form of a dictionary to an AVL tree."""
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
def example_move():
    level = 2
    data_dict = dict()
    prev_weak_arm, prev_strong_arm = (0, 0), (0, 0)
    return Move(example_universe, example_main_character, level, data_dict, prev_weak_arm, prev_strong_arm)


@pytest.fixture
def mock_universe():
    """ This replaces (mocks) the methods boss_enemies_aid_help_charter_armor_position and field in Universe. """
    def temp1(x):
        return b_p, e_p, a_p, h_p, w_p+s_p

    @property
    def temp2(x):
        f = [[cs.no_path for _ in range(20)] for _ in range(50)]
        for p in v_p:
            f[p[0]][p[1]] = cs.path
        for p in e_p:
            f[p[0]][p[1]] = random.choice([cs.regular_enemy, cs.unknown])
        for p in a_p+w_p+s_p:
            f[p[0]][p[1]] = random.choice([cs.aid, cs.unknown])
        for p in h_p:
            f[p[0]][p[1]] = random.choice([cs.helper_character, cs.unknown])
        f[0][0] = cs.main_character
        return f

    def temp3(s, x):
        if x not in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            return "BAGABAGABOBO"
        if not s._field:
            f = [[cs.no_path for _ in range(20)] for _ in range(50)]
            for p in v_p:
                f[p[0]][p[1]] = cs.path
            for p in e_p:
                f[p[0]][p[1]] = random.choice([cs.regular_enemy, cs.unknown])
            for p in a_p + w_p + s_p:
                f[p[0]][p[1]] = random.choice([cs.aid, cs.unknown])
            for p in h_p:
                f[p[0]][p[1]] = random.choice([cs.helper_character, cs.unknown])
            f[0][0] = cs.main_character
        else:
            f = s._field
        main_pos = [(i, j) for i, row in enumerate(f) for j, cell in enumerate(row) if cell in [cs.main_character, cs.fight]][0]
        if f[main_pos[0]][main_pos[1]] == cs.fight:
            return
        elif f[main_pos[0] + x[0]][main_pos[1] + x[1]] in [cs.path, cs.aid, cs.helper_character]:
            f[main_pos[0]][main_pos[1]] = cs.path
            f[main_pos[0] + x[0]][main_pos[1] + x[1]] = cs.main_character
        elif f[main_pos[0] + x[0]][main_pos[1] + x[1]] in [cs.boss, cs.unknown, cs.regular_enemy]:
            f[main_pos[0]][main_pos[1]] = cs.path
            f[main_pos[0] + x[0]][main_pos[1] + x[1]] = cs.fight
        s._field = f
        return

    with mock.patch.multiple('src.Intermediate.Universe_Construction.Universe',
                             boss_enemies_aid_help_charter_armor_position=temp1, field=temp2, update_field=temp3) \
            as mocks:
        yield mocks


@pytest.mark.parametrize("level, prev_weak, prev_strong",
                         [(2, (0, 0), (0, 0)),
                          (1, (400, 400), (600, 600)),
                          (4, (50, 50), (6000, 5000)),
                          ])
def test_correct_initialization(mock_universe, example_universe, example_main_character, example_tree, level, prev_weak, prev_strong):
    m = Move(example_universe, example_main_character, level, example_tree, prev_weak_arm=prev_weak,
             prev_strong_arm=prev_strong)
    assert isinstance(m.field, Universe)
    assert isinstance(m.mapping, Assignments)
    assert isinstance(m.player, MainCharacter)
    assert m.extra_helper_characters == []
    for pos in e_p:
        assert isinstance(m.mapping.get_enemy(pos), BadCharacter)
    for pos in a_p:
        assert isinstance(m.mapping.get_aid(pos), Aid)
    for pos in h_p:
        assert isinstance(m.mapping.get_helper_char(pos), GoodCharacter)
    for pos in w_p:
        assert isinstance(m.mapping.get_armor(pos), Weapon)
    for pos in s_p:
        assert isinstance(m.mapping.get_armor(pos), Shield)


@pytest.mark.parametrize("field, player, level, data_tree, prev_weak, prev_strong",
                         [((True, True), (False, 0), 2, (False, 5), (0, 0), (0, 0)),
                          ((False, False), (True, "Wrong_type_player"), 1, (False, False), (400, 400), (600, 600)),
                          ((False, False), (False, False), 1, (True, 5), (400, 400), (600, 600)),
                          ((False, False), (False, False), True, (False, 5), (400, 400), (600, 600)),
                          ((False, False), (False, False), 1, (False, 5), (400, 400, 7), (600, 600)),
                          ((False, False), (False, False), 1, (False, 5), (400, 400), (600, "Hello")),
                          ])
def test_wrong_initialization(mock_universe, example_universe, example_main_character, example_tree, field, player,
                              level, data_tree, prev_weak, prev_strong):
    u = field[1] if field[0] else example_universe
    p = player[1] if player[0] else example_main_character
    t = data_tree[1] if data_tree[0] else example_tree
    if (not (field[0] and player[0] and data_tree[0]) and not field[0] == player[0] == data_tree[0]) or \
            (type(level) != int or level < 1):
        with pytest.raises(TypeError):
            m = Move(u, p, level, t, prev_weak_arm=prev_weak, prev_strong_arm=prev_strong)
    else:
        with pytest.raises(ValueError):
            m = Move(u, p, level, t, prev_weak_arm=prev_weak, prev_strong_arm=prev_strong)


@pytest.mark.parametrize("s, d, mag",
                         [(cs.multi_step[0], cs.directions[1][0], str(5)),
                          (cs.one_step[0], cs.directions[2][0], str(1)),
                          (cs.multi_step[1], cs.directions[2][1], str(5)),
                          (cs.one_step[1], cs.directions[1][1], str(1)),
                          (cs.multi_step[1], cs.directions[0][1], str(5)),
                          (cs.one_step[1], cs.directions[3][1], str(1)),
                          ])
def test_correct_step(mock_universe, example_universe, example_main_character, example_tree, s, d, mag):
    m = Move(example_universe, example_main_character, 2, example_tree, prev_weak_arm=(400, 400),
             prev_strong_arm=(600, 600))
    if s in cs.multi_step:
        step_comm = s + mag + " " + d
    else:
        step_comm = s + d
    m.step(step_comm)
    if d in cs.directions[2]:
        assert m.field._field[0][1] == cs.fight
        for row in m.field._field:
            assert cs.main_character not in row
    elif d in cs.directions[1]:
        assert m.field._field[int(mag)][0] == cs.main_character
    else:
        assert m.field._field[0][0] == cs.main_character
        for row in m.field._field[1:]:
            assert cs.main_character not in row
            assert cs.fight not in row
