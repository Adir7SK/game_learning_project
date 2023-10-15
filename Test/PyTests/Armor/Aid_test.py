import pytest

from src.Common_general_functionalities.common_strings import aid_types
from src.Armor.Aid import Aid
import src.Common_general_functionalities.common_strings as cs


@pytest.mark.parametrize("name, aid_number, mag",
                         [(cs.health, 0, 3),
                          (cs.energy, 1, 2),
                          (cs.strength, 2, 1),
                          (cs.speed, 3, 0),
                          (cs.shield, 4, 4),
                          ])
def test_serial_number_check(name, aid_number, mag):
    aid = Aid(name, aid_types[aid_number], mag)
    assert (aid.serial_number())[:3] == cs.aid_ser and 0 < float((aid.serial_number())[3:]) < 100


@pytest.mark.parametrize("name, aid_number, mag",
                         [(cs.health, 0, 3),
                          (cs.energy, 1, 2),
                          (cs.strength, 2, 1),
                          (cs.speed, 3, 0),
                          (cs.shield, 4, 4),
                          ])
def test_activate(name, aid_number, mag):
    aid = Aid(name, aid_types[aid_number], mag)
    a, m = aid.activate()
    assert a in aid_types and 0 < m < 100
    assert (None, 0) == (aid.activate())


@pytest.mark.parametrize("name, aid_number, mag",
                         [(cs.health, 0, 3),
                          (cs.energy, 1, 2),
                          (cs.strength, 2, 1),
                          (cs.speed, 3, 0),
                          (cs.shield, 4, 4),
                          ])
def test_name(name, aid_number, mag):
    aid = Aid(name, aid_types[aid_number], mag)
    assert aid.name() == name


@pytest.mark.parametrize("name, aid_number, mag",
                         [(cs.health, 0, 3),
                          (cs.energy, 1, 2),
                          (cs.strength, 2, 1),
                          (cs.speed, 3, 0),
                          (cs.shield, 4, 4),
                          ])
def test_aid_type_getter(name, aid_number, mag):
    aid = Aid(name, aid_types[aid_number], mag)
    assert aid.aid_type == aid_types[aid_number]


@pytest.mark.parametrize("name, aid_number, mag",
                         [(cs.health, 0, 3),
                          (cs.energy, 1, 2),
                          (cs.strength, 2, 1),
                          (cs.speed, 3, 0),
                          (cs.shield, 4, 4),
                          ])
def test_aid_type_setter(name, aid_number, mag):
    aid = Aid(name, aid_types[aid_number], mag)
    with pytest.raises(AttributeError):
        aid.aid_type = aid_types[2]
