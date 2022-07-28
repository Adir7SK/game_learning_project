import sys


class Node:
    def __init__(self, serial_number, obj):
        self.serial_number = serial_number
        self.obj = obj
        self.right = None
        self.left = None
        self.height = 1

    def __repr__(self):
        return f"Serial Number: {self.serial_number}, Object's name: {self.obj.name}"


class AVL:
    """
    Adelson-Velsky and Landis (AVL) tree is a self-balancing tree; from each node, the difference in height
    from either side to the last node is at most 1.
    Balance factor of a node is the difference in height between the left and right subtree from that node.
    Therefore, the balance factor should stay either 1, 0, or -1.
    This will be used so user can add an item to the tree, and that we can see which item is the next in the
    data (i.e. the tree) regarding strength, when the player gets stronger.
    """
    def insert(self, tree, val, obj):
        if not obj.name:
            raise AttributeError("The object must have a name")
        if type(val) != int or val < 1:
            raise AttributeError("Invalid Serial Number.")
        if tree is None:
            return Node(val, obj)
        elif val < tree.serial_number:
            tree.left = self.insert(tree.left, val, obj)
        elif val > tree.serial_number:
            tree.right = self.insert(tree.right, val, obj)
        else:
            raise ValueError("Serial number already exists")
            
        tree.height = 1 + max(self.get_height(tree.left), self.get_height(tree.right))
        
        balance = self.balance(tree)
        
        if balance > 1 and tree.left.serial_number > val:
            return self.right_rotation(tree)
        if balance < -1 and val > tree.right.serial_number:
            return self.left_rotation(tree)
        if balance > 1 and val > tree.left.serial_number:
            tree.left = self.left_rotation(tree.left)
            return self.right_rotation(tree)
        if balance < -1 and val < tree.right.serial_number:
            tree.right = self.right_rotation(tree.right)
            return self.left_rotation(tree)
        return tree

    def right_rotation(self, tree_part):
        a = tree_part.left
        b = a.right
        a.right = tree_part
        tree_part.left = b
        
        tree_part.height = 1 + max(self.get_height(tree_part.left), self.get_height(tree_part.right))
        a.height = 1 + max(self.get_height(a.left), self.get_height(a.right))
        return a

    def left_rotation(self, tree_part):
        a = tree_part.right
        b = a.left
        a.left = tree_part
        tree_part.right = b

        tree_part.height = 1 + max(self.get_height(tree_part.left), self.get_height(tree_part.right))
        a.height = 1 + max(self.get_height(a.left), self.get_height(a.right))
        return a

    @staticmethod                           # It only operates inside the class and does not need self
    def get_height(tree_part):
        if not tree_part:
            return 0
        return tree_part.height

    def balance(self, tree_part):
        if not tree_part:
            return 0
        return self.get_height(tree_part.left) - self.get_height(tree_part.right)
        
    def search(self, tree, serial_number):
        if type(serial_number) != int:
            raise TypeError("Serial number must be an integer.")
        if not tree:
            return False
        if tree.serial_number == serial_number:
            return tree.obj
        elif tree.serial_number < serial_number:
            return self.search(tree.right, serial_number)
        else:
            return self.search(tree.left, serial_number)

    def preorder(self, tree):
        if tree is None:
            return
        print(tree.serial_number)
        self.preorder(tree.left)
        self.preorder(tree.right)

    # Prints the tree
    def print_helper(self, curr_ptr, indent="", last=True):
        """Call this method as follows: AVL().print_helper(tree)"""
        if curr_ptr is not None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(curr_ptr.serial_number, curr_ptr.obj.name)
            self.print_helper(curr_ptr.left, indent, False)
            self.print_helper(curr_ptr.right, indent, True)
               

class BasicObject:
    def __init__(self, name):
        self.name = name
        
    def name(self):
        return self.name
