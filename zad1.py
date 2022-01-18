


class Binary_Tree():
    """Biniary tree class"""

    def __init__(self, item, parent=None):
        self.key = item
        self.count = 1
        self.left_child = None
        self.right_child = None
        self.parent = parent
        self.tree = [self.key, self.left_child, self.right_child]

    def get_root(self):
        """Returns the root of the tree"""
        return self.key

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count

    def set_root(self, value):
        """Method set value of root"""
        self.key = value

    def get_parent(self):
        """Returns the parent of the tree"""
        return self.parent

    def set_parent(self, value):
        """Method set parent of the tree"""
        self.parent = value

    def get_children_number(self):
        """Returns the number of children"""
        n = 0
        if self.right_child != None:
            n += 1
        if self.left_child != None:
            n += 1
        return n

    def get_left_branch(self):
        """Returns left branch of tree"""
        return self.left_child

    def get_right_branch(self):
        """Returns right branch of tree"""
        return self.right_child

    def set_right_branch(self, item):
        """Method set right branch of tree"""
        self.right_child = item

    def set_left_branch(self, item):
        """Method set left branch of tree"""
        self.left_child = item

    def insert_left(self, item):
        """Inserts left branch of tree"""
        if self.left_child == None:
            self.left_child = Binary_Tree(item, self)

        else:
            temp_tree = Binary_Tree(item, self)
            temp_tree.left_child = self.left_child
            self.left_child = temp_tree

    def insert_right(self, item):
        """Inserts right branch of tree"""
        if self.right_child == None:
            self.right_child = Binary_Tree(item, self)
        else:
            temp_tree = Binary_Tree(item, self)
            temp_tree.right_child = self.right_child
            self.right_child = temp_tree

    def add_element(self, item):
        """Add an element to the tree"""
        temp_tree = self
        before_tree = self
        while True:
            if temp_tree.get_root() == item:
                temp_tree.set_count(temp_tree.get_count() + 1)
                return

            elif temp_tree.get_root() > item:
                before_tree = temp_tree
                temp_tree = temp_tree.get_left_branch()
                if temp_tree == None:
                    before_tree.insert_left(item)
                    break

            else:
                before_tree = temp_tree
                temp_tree = temp_tree.get_right_branch()
                if temp_tree == None:
                    before_tree.insert_right(item)
                    break

    def delate(self, item):
        """Delete item from tree"""
        temp_tree = self
        try:
            while True:  # dopisać jak nie zawiera
                if item == temp_tree.get_root():
                    if temp_tree.get_count() > 1:
                        temp_tree.set_count(temp_tree.get_count() - 1)
                        return
                    else: 
                        break
                if temp_tree.get_root() > item:
                    temp_tree = temp_tree.get_left_branch()
                else:
                    temp_tree = temp_tree.get_right_branch()
        except:
            raise ValueError("This element does not exist")

        if temp_tree.get_children_number() == 0:
            if temp_tree.parent.get_root() >= item:
                temp_tree.parent.set_left_branch(None)
            else:
                temp_tree.parent.set_right_branch(None)

        elif temp_tree.get_children_number() == 1:
            if temp_tree.parent.get_root() >= item:
                if temp_tree.get_left_branch() == None:
                    temp_tree.parent.set_left_branch(temp_tree.get_right_branch())
                    temp_tree.get_right_branch().parent = temp_tree.parent
                else:
                    temp_tree.parent.set_left_branch(temp_tree.get_left_branch())
                    temp_tree.get_left_branch().parent = temp_tree.parent
            else:
                if temp_tree.get_left_branch() == None:
                    temp_tree.parent.set_right_branch(temp_tree.get_right_branch())
                    temp_tree.get_right_branch().parent = temp_tree.parent
                else:
                    temp_tree.parent.set_right_branch(temp_tree.get_left_branch())
                    temp_tree.get_left_branch().parent = temp_tree.parent


        else:
            root_to_delate = temp_tree
            temp_tree = temp_tree.get_right_branch()
            while temp_tree.get_left_branch() != None:
                temp_tree = temp_tree.get_left_branch()

            root_to_delate.set_root(temp_tree.get_root())

        return

    def __delitem__(self, key):
        self.delate(key)

    def __contains__(self, item):
        """Check if the given item is in the tree"""

        temp_tree = self
        try:
            while True:
                if item == temp_tree.get_root():
                    return True
                if temp_tree.get_root() > item:
                    temp_tree = temp_tree.get_left_branch()
                else:
                    temp_tree = temp_tree.get_right_branch()
        except:
            return False

    def __getitem__(self, key):
        self.tree = [self.key, self.left_child, self.right_child]
        return self.tree[key]

    def __str__(self):
        """Return a string representation of this tree in preorder way"""
        self.string = ''

        def preorder(tree):
            if tree:
                self.string += str(tree.key)+', '
                preorder(tree.get_left_branch())
                preorder(tree.get_right_branch())
            # else:
            #     self.string += 'None, '

        preorder(self)

        return self.string


if __name__ == '__main__':
    my_tree = Binary_Tree(5)
    print(my_tree)
    my_tree.insert_right(8)
    print(my_tree)
    my_tree.add_element(7)
    print(my_tree)
    my_tree.add_element(3)
    my_tree.add_element(7)
    my_tree.add_element(9)
    my_tree.add_element(2)
    my_tree.add_element(4)
    print(my_tree)
    print(my_tree[2][2][0])
    print(5 in my_tree)
    print(3 in my_tree)
    print(7 in my_tree)
    print(9 in my_tree)
    print(8 in my_tree)
    print(11 in my_tree)
    my_tree.delate(9)
    print(my_tree)
    my_tree.delate(7)
    print(my_tree)
    my_tree.delate(7)
    print(my_tree)
    my_tree.delate(3)
    print(my_tree)
    # my_tree.add_element(4)
    # A = []
    # print(A)
