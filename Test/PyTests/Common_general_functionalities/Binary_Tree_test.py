import pytest
from src.Common_general_functionalities import common_strings as cs
from src.Common_general_functionalities.Binary_Tree import AVL, BasicObject


class WrongObject:
    def __init__(self, random_value):
        self.random_value = random_value

    def random_value(self):
        return self.random_value


@pytest.fixture
def full_tree():
    """Creating a data fixture as AVL tree."""
    global AVLTree
    AVLTree = AVL()
    tree = None
    tree = AVLTree.insert(tree, 10, BasicObject(cs.efficient + " " + cs.sword))
    tree = AVLTree.insert(tree, 9, BasicObject(cs.sloppy + " " + cs.gun))
    tree = AVLTree.insert(tree, 15, BasicObject(cs.efficient + " " + cs.gun))
    tree = AVLTree.insert(tree, 5, BasicObject(cs.sloppy + " " + cs.sword))
    tree = AVLTree.insert(tree, 12, BasicObject(cs.sloppy + " Machine Gun"))
    return tree


@pytest.mark.parametrize("serial_n, expected_name",
                         [(9, cs.sloppy + " " + cs.gun),
                          (5, cs.sloppy + " " + cs.sword),
                          (10, cs.efficient + " " + cs.sword),
                          (12, cs.sloppy + " Machine Gun"),
                          (15, cs.efficient + " " + cs.gun),
                          ])
def test_search_on_tree(full_tree, serial_n, expected_name):
    """Searching a valid existing serial number works."""
    assert AVLTree.search(full_tree, serial_n).name == expected_name


@pytest.mark.parametrize("serial_n", [4, 2, 1000, 3])
def test_search_index_that_doesnt_exists(full_tree, serial_n):
    """searching a valid but non-existing serial number returns False."""
    assert AVLTree.search(full_tree, serial_n) is False


@pytest.mark.parametrize("serial_n", [4.5, "2", [1000], {3: 3}])
def test_search_index_with_wrong_data_type(full_tree, serial_n):
    """Searching an invalid serial number raises a Type Error."""
    with pytest.raises(TypeError):
        AVLTree.search(full_tree, serial_n)


@pytest.mark.parametrize("serial_n, input_obj_name",
                         [(4.5, cs.sloppy),
                          ("2", cs.sword),
                          ([1000], cs.efficient),
                          ({3: 3}, "Machine Gun"),
                          ])
def test_insert_invalid_index(full_tree, serial_n, input_obj_name):
    """Insertion with invalid serial number type raises an attribute error."""
    with pytest.raises(AttributeError):
        AVLTree.insert(full_tree, serial_n, BasicObject(input_obj_name))


@pytest.mark.parametrize("serial_n, input_obj",
                         [(4, cs.sloppy),
                          (2, WrongObject(cs.sword)),
                          (1000, [cs.efficient]),
                          (3, 5),
                          ])
def test_insert_invalid_object(full_tree, serial_n, input_obj):
    """Insertion with invalid object raises an attribute error."""
    with pytest.raises(AttributeError):
        AVLTree.insert(full_tree, serial_n, input_obj)
