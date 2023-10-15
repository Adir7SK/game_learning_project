import pytest
from src.Data_Loading.Data_Placement import GameDetailsData
from src.Armor.Weapon import Weapon
from src.Armor.Shield import Shield
from src.Armor.Aid import Aid
from src.Characters.Good_Character import GoodCharacter
from src.Common_general_functionalities import common_strings as cs


"""
Here we shall test the following:
    1. Attribute undercover datatype testing                                
    2. Initializing with wrong items                                        
    3. Does the item function returns all the items                         
    4. Is undercover getter and setter works                                
    5. Validating getter and setter for weapon and shield                   
    6. Validating getter and setter for energy                              
    7. Validating renew-energy                                              
    8. Validate the functionalities of life attribute (that couldn't be tested in the abstract parent class Character)
    9. Validate the functionalities of alive attribute (that couldn't be tested in the abstract parent class Character)
"""
global_weapon = GameDetailsData().load_weapons().weapon_collection.right.obj
global_shield = GameDetailsData().load_shields().shield_collection.right.obj
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
    for i in ite:
        if (i[1])[:6] not in [cs.weapon, cs.shield] and (i[1])[:3] != cs.aid_ser:
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


@pytest.mark.parametrize("setget, correct, relevant_object",
                         [(True, True, GameDetailsData().load_weapons().weapon_collection.left.obj),
                          (True, True, GameDetailsData().load_weapons().weapon_collection.obj),
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
        assert ((GameDetailsData().get_armor_data())[cs.weapons].search(ser)).armor_efficiency() == expected
    else:
        assert round(example_good_character.weapon.armor_efficiency(), 8) == expected


@pytest.mark.parametrize("setget, correct, relevant_object",
                         [(True, True, GameDetailsData().load_shields().shield_collection.left.obj),
                          (True, True, GameDetailsData().load_shields().shield_collection.obj),
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
        assert ((GameDetailsData().get_armor_data())[cs.weapons].search(ser)).armor_efficiency() == expected
    else:
        assert round(example_good_character.shield.armor_efficiency(), 8) == expected


@pytest.mark.parametrize("step, repetitions, value, expected",
                         [(True, 4, 10, 92),
                          (True, 80, 5.5, 12.0),
                          (False, 3, 0, 97.72),
                          (False, 5, 1, 93.3),
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
    Testing that the damaging character's life operates correctly.
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
    Testing that repetitive damage to character's life operates correctly.
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


@pytest.mark.parametrize("start_life, damage, life_left",
                         [(100, 50, 50),
                          (23.3, 10, 13.3),
                          ])
def test_life(start_life, damage, life_left):
    c = GoodCharacter(start_life, False)
    c.life = damage
    assert c._full_life == start_life
    assert c.life == life_left


@pytest.mark.parametrize("start_life", ["100", [100], -45, 0])
def test_wrong_life_initialization(start_life):
    with pytest.raises(TypeError):
        c = GoodCharacter(start_life, False)


@pytest.mark.parametrize("start_life, damage", [(100, 500), (23.3, 23.3)])
def test_alive(start_life, damage):
    c = GoodCharacter(start_life, False)
    assert c.alive
    c.life = damage
    assert not c.alive


@pytest.mark.parametrize("undercover, symbol", [(True, cs.unknown), (False, cs.helper_character)])
def test_character_symbol(undercover, symbol):
    c = GoodCharacter(100, undercover)
    assert c.symbol == symbol
