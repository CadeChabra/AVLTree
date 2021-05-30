import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random

class AVLTree:

    def __init__ (self):
        self.root = None
        self._size = 0

    # Adds a new node with the given value using AVL balancing algorithm if necessary
    ########################################################################
    # Parameters:
    # int or float
    ########################################################################
    # Return:
    # True if parameters are valid and the node was successfully added
    # False if paramters are invalid and the node was not added
    ########################################################################
    def add_node (self, val):

        # Returns False if the parameters are not of the correct type
        # Otherwise continues with addition process and returns true
        if type(val) is not int and type(val) is not float:
            return False
        else: 
            # If the tree is empty, then set the root to be the new node
            # Otherwise continue with additon process
            if self.root is None:
                self.root = AVLNode(val)
            else:
                # Creates curr variable to trace through tree with
                curr = self.root
                # Trace through the tree to find spot for new node, then insert the node when the spot is found
                while True:
                    if val <= curr.get_value():
                        if curr.get_left() == None:
                            curr.set_left(AVLNode(val))
                            curr.get_left().set_parent(curr)
                            break
                        else:
                            curr = curr.get_left()
                    else:
                        if curr.get_right() == None:
                            curr.set_right(AVLNode(val))
                            curr.get_right().set_parent(curr)
                            break
                        else:
                            curr = curr.get_right()
                # Trace backwards through the tree adjusting the height values and checking to see if a rotation is necessary
                while curr is not None:
                    # If curr has two children, make the height of curr 1 more than the height of the taller child
                    # Then check for an imbalance and call for a rotation if necessary
                    if curr.get_left() is not None and curr.get_right() is not None:
                        curr.set_height(max(curr.get_left().get_height(), curr.get_right().get_height()) + 1)
                        if abs(curr.get_left().get_height() - curr.get_right().get_height()) >= 2:
                            self.__rotate(curr)
                    # If the left child is null, make the height of curr 1 more than the height of the right child
                    # Then check for an imbalance and call for a rotation if necessary
                    elif curr.get_left() is None and curr.get_right() is not None:
                        curr.set_height(curr.right.height + 1)
                        if curr.get_right().get_height() >= 1:
                            self.__rotate(curr)
                    # If the right child is null, make the height of curr 1 more than the height of the left child
                    # Then check for an imbalance and call for a rotation if necessary
                    elif curr.get_right() is None and curr.get_left() is not None:
                        curr.set_height(curr.left.height + 1)
                        if curr.get_left().get_height() >= 1:
                            self.__rotate(curr)
                    # If the current node has no children, it is a leaf with height 0
                    else:
                        curr.set_height(0)
                    # Move curr upwards to check next node
                    curr = curr.get_parent()
            self._size += 1
            return True

    # Deletes a first instance of a node with the given value using the AVL balancing algorithm if necessary
    ########################################################################
    # Parameters:
    # int or float
    ########################################################################
    # Return:
    # True if node with the given value exists and was successfully deleted
    # False if node with the given value does not exist
    ########################################################################
    def del_node (self, val):
        # Returns false if the given value is not an int or float
        # Otherwise continues with deletion and returns true
        if type(val) is not int and type(val) is not float:
            return False
        else:
            # Creates deleted varaible to track whether or not deletion is successful
            deleted = False
            # Creates curr variable to trace through tree
            curr = self.root
            # Trace through tree searching for node to be deleted
            while curr is not None:
                # If current value equals val, delete the node then rotate if necessary
                if val == curr.get_value():
                    # Deletes node
                    # If node is leaf, unlink node from parent
                    if curr.get_left() is None and curr.get_right() is None:
                        # Node is root
                        if curr is self.root:
                            self.root = None
                        # Node is a left child
                        elif curr.get_parent().get_left() is curr:
                            curr.get_parent().set_left(None)
                        # Node is a right child
                        else:
                            curr.get_parent().set_right(None)
                    # If node has only a left child, replace node with left child and unlink all references to node
                    elif curr.get_right() is None and curr.get_left() is not None:
                        # Node is root
                        if curr is self.root:
                            self.root = curr.get_left()
                            self.root.set_parent(None)
                        # Node is left child
                        elif curr.get_parent().get_left() is curr:
                            curr.get_parent().set_left(curr.get_left())
                            curr.get_left().set_parent(curr.get_parent())
                        # Node is right child
                        else:
                            curr.get_parent().set_right(curr.get_left())
                            curr.get_left().set_parent(curr.get_parent())
                    # If node has only a right child, replace node with right child and unlink all references to node
                    elif curr.get_left() is None and curr.get_right() is not None:
                        # Node is root
                        if curr is self.root:
                            self.root = curr.right
                            self.root.set_parent(None)
                        # Node is left child
                        elif curr.get_parent().get_left() is curr:
                            curr.get_parent().set_left(curr.get_right())
                            curr.get_right().set_parent(curr.get_parent())
                        # Node is right child
                        else:
                            curr.get_parent().set_right(curr.right)
                            curr.get_right().set_parent(curr.parent)
                    # If node has both children, replace with in-order predecessor (or successor if there is not predecessor)
                    else:
                        # Create a variable repl to store the node which will replace curr
                        # By default, the replacement is curr's left child
                        repl = curr.get_left()
                        # Trace down the rightmost path of curr's left child to find the in-order predecessor of curr
                        while repl.get_right() is not None:
                            repl = repl.get_right()
                        # Replacement is curr's left child
                        if repl is curr.get_left():
                            repl.set_right(curr.get_right())
                            repl.get_right().set_parent(repl)
                            # Curr is root
                            if curr is self.root:
                                self.root = repl
                                repl.set_parent(None)
                            # Curr is left child
                            elif curr is curr.get_parent().get_left():
                                curr.get_parent().set_left(repl)
                                repl.set_parent(curr.get_parent())
                            # Curr is right child
                            else:
                                curr.get_parent().set_right(repl)
                                repl.set_parent(curr.parent)
                            # Set parent of curr to be repl for back-tracing purposes
                            curr.set_parent(repl)
                        # Replacement is a right child
                        else:
                            repl.set_right(curr.get_right())
                            repl.get_right().set_parent(repl)
                            repl.get_parent().set_right(None)
                            # Replacement node has no left child
                            if repl.get_left() is None:
                                repl.set_left(curr.get_left())
                                repl.get_left.set_parent(repl)
                            # Replacement node has a left child
                            else:
                                repl.get_left().set_left(curr.get_left())
                                repl.get_left().get_left().set_parent(repl.get_left())
                            # Curr is root
                            if curr is self.root:
                                self.root = repl
                                repl.set_parent(None)
                            # Curr is a left child
                            elif curr.get_parent().get_left() is curr:
                                curr.get_parent().set_left(repl)
                                repl.set_parent(curr.get_parent())
                            # Curr is a right child
                            else:
                                curr.get_parent().set_right(repl)
                                repl.set_parent(curr.parent)
                            # Set parent to be left-left grandchild of replacement in order to start back tracing from there
                            curr.set_parent(repl.get_left().get_left())
                    # Traces backwards through the tree adjusting heights, checking for imbalances and rotating if necessary
                    # Set curr equal to the node its parent (which will be the node that replaced it) to start tracing
                    curr = curr.get_parent()
                    while curr is not None:
                        # If curr has two children, make the height of curr 1 more than the height of the taller child
                        # Then check for an imbalance and call for a rotation if necessary
                        if curr.get_left() is not None and curr.get_right() is not None:
                            curr.set_height(max(curr.left.height, curr.right.height) + 1)
                            if abs(curr.get_left().get_height() - curr.get_right().get_height()) >= 2:
                                self.__rotate(curr)
                        # If the left child is null, make the height of curr 1 more than the height of the right child
                        # Then check for an imbalance and call for a rotation if necessary
                        elif curr.get_left() is None and curr.get_right() is not None:
                            curr.set_height(curr.get_right().get_height() + 1)
                            if curr.get_right().get_height() >= 1:
                                self.__rotate(curr)
                        # If the right child is null, make the height of curr 1 more than the height of the left child
                        # Then check for an imbalance and call for a rotation if necessary
                        elif curr.get_right() is None and curr.get_left() is not None:
                            curr.set_height(curr.get_left().get_height() + 1)
                            if curr.get_left().get_height() >= 1:
                                self.__rotate(curr)
                        # If both children are null, make the height of curr 0
                        else:
                            curr.set_height(0)
                        # Move curr upwards to check next node
                        curr = curr.get_parent()
                    # After successfully deleting the node and rotating if necessary, decrement the tree size, break the loop, and return true
                    self._size -= 1
                    deleted = True
                    break
                # If val is greater than current value, set curr equal to its right child and iterate
                elif val > curr.get_value():
                    curr = curr.get_right()
                # If val is less than current value, set curr equal to its left child and iterate
                else:
                    curr = curr.get_left()
            return deleted

    # Returns an array of sorted values in the tree
    # Uses recursive sort method of AVLNode class
    def sort (self):
        if self.root is None:
            return []
        else:
            return self.root.recursive_sort([])
            
    # Returns the height of the entire tree
    # Returns -1 if the tree is empty
    def get_tree_height(self):
        ht = -1
        if self.root is not None:
            ht = self.root.get_height()
        return ht

    # Returns the number of nodes in the tree
    def size(self):
        return self._size

    # Draws the tree in a Qt GUI window
    def draw (self):
        app = QApplication(sys.argv)
        win = QWidget()
        win.resize(1600,800)
        win.setWindowTitle("AVL Tree")
        if self.root is not None:
            self.root.recursive_draw(800, 50, 0, win)
        win.show()
        sys.exit(app.exec_())

    # Returns the maximum value in the tree
    def get_max (self):
        max = self.root
        if max is not None:
            while max.get_right() is not None:
                max = max.get_right()
            return max.get_value()
        return None

    # Returns the minimum value in the tree
    def get_min (self):
        max = self.root
        if max is not None:
            while max.get_left() is not None:
                max = max.get_left()
            return max.get_value()
        return None

    # Performs a rotation on the given node
    # Supporting method used in add_node and del_node
    def __rotate (self, node):
        # Left rotation
        if node.get_right() is None or (node.get_left() is not None and node.get_left().get_height() > node.get_right().get_height()):
            # Left-left rotation
            if node.get_left().get_right() is None or (node.get_left().get_left() is not None and node.get_left().get_left().get_height() > node.get_left().get_right().get_height()):
                # Left-left rotation with node as root
                if node is self.root:
                    self.root = node.get_left()
                    node.set_left(self.root.get_right())
                    self.root.set_right(node)
                    node.set_parent(self.root)
                    self.root.set_parent(None)
                    if node.get_left() is not None:
                        node.get_left().set_parent(node)
                # Left-left rotation with node not as root
                else:
                    # Node is a left child
                    if node.get_parent().get_left() is node:
                        node.get_parent().set_left(node.get_left())
                        node.set_left(node.get_parent().get_left().get_right())
                        node.get_parent().get_left().set_right(node)
                        node.get_parent().get_left().set_parent(node.get_parent())
                        node.set_parent(node.get_parent().get_left())
                        if node.get_left() is not None:
                            node.get_left().set_parent(node)
                    # Node is a right child
                    else:
                        node.get_parent().set_right(node.left)
                        node.set_left(node.get_parent().get_right().get_right())
                        node.get_parent().get_right().set_right(node)
                        node.get_parent().get_right().set_parent(node.get_parent())
                        node.set_parent(node.get_parent().get_right())
                        if node.get_left() is not None:
                            node.get_left().set_parent(node)
                # Adjusts height of node after left-left rotation
                if node.get_right() is None:
                    # Node is leaf is it has no right child after a left-left rotation
                    node.set_height(0)
                elif node.get_left() is None:
                    # Node height is one more than height of right node if there is no left node
                    node.set_height(node.get_right().get_height() + 1)
                else:
                    # Node height is one more than the greater of its children's heights if both children exist
                    node.set_height(max(node.get_left().get_height(), node.get_right().get_height()) + 1)
            # Left-right rotation (double rotation)
            else:
                # First Rotation
                node.set_left(node.get_left().get_right())
                node.get_left().get_parent().set_right(node.get_left().get_left())
                node.get_left().set_left(node.get_left().get_parent())
                node.get_left().get_left().set_parent(node.get_left())
                node.get_left().set_parent(node)
                if node.get_left().get_left().get_right() is not None:
                    node.get_left().get_left().get_right().set_parent(node.get_left().get_left())
                # Adjusts height of original left node after first rotation
                if node.get_left().get_left().get_left() is None and node.get_left().get_left().get_right() is not None:
                    # If only the right child exists, height is one more than the right child's
                    node.get_left().get_left().set_height(node.get_left().get_left().get_right().get_height() + 1)
                elif node.get_left().get_left().get_right() is None and node.get_left().get_left().get_left() is not None:
                    # If only the left child exists, height is one more than the left child's
                    node.get_left().get_left().set_height(node.get_left().get_left().get_left().get_height() + 1)
                elif node.get_left().get_left().get_left() is None and node.get_left().get_left().get_right() is None:
                    # If neither child exists, height is 0
                    node.get_left().get_left().set_height(0)
                else:
                    # If both children exist, height is one more than the greater of its children's heights
                    node.get_left().get_left().set_height(max(node.left.left.left.height, node.left.left.right.height))
                # Second rotation with node as root
                if node is self.root:
                    self.root = node.get_left()
                    node.set_left(self.root.get_right())
                    self.root.set_right(node)
                    node.set_parent(self.root)
                    self.root.set_parent(None)
                    if node.get_left() is not None:
                        node.get_left().set_parent(node)
                # Second rotation with node not as root
                else:
                    # Node is a left child
                    if node.get_parent().get_left() is node:
                        node.get_parent().set_left(node.get_left())
                        node.set_left(node.get_parent().get_left().get_right())
                        node.get_parent().get_left().set_right(node)
                        node.get_parent().get_left().set_parent(node.get_parent())
                        node.set_parent(node.get_parent().get_left())
                        if node.get_left() is not None:
                            node.get_left().set_parent(node)
                    # Node is a right child
                    else:
                        node.get_parent().set_right(node.get_left())
                        node.set_left(node.get_parent().get_right().get_right())
                        node.get_parent().get_right().set_right(node)
                        node.get_parent().get_right().set_parent(node.get_parent())
                        node.set_parent(node.get_parent().get_right())
                        if node.get_left() is not None:
                            node.get_left().set_parent(node)
                # Adjusts height of node after left-right rotation
                if node.get_left() is None and node.get_right() is not None:
                    # If only the right child exists, height is one more than the right child's
                    node.set_height(node.get_right().get_height() + 1)
                elif node.get_right() is None and node.get_left() is not None:
                    # If only the left child exists, height is one more than the left child's
                    node.set_height(node.get_left().get_height() + 1)
                elif node.get_right() is None and node.get_left() is None:
                    # If neither child exists, height is 0
                    node.set_height(0)
                else:
                    # If both children exist, height is one more than the greater of the children's heights
                    node.set_height(max(node.get_left().get_height(), node.get_right().get_height()))
        # Right rotation
        else:
            # Right-right rotation
            if node.get_right().get_left() is None or (node.get_right().get_right() is not None and node.get_right().get_right().get_height() > node.get_right().get_left().get_height()):
                # Right-right rotation with node as root
                if node is self.root:
                    self.root = node.get_right()
                    node.set_right(self.root.get_left())
                    self.root.set_left(node)
                    node.set_parent(self.root)
                    self.root.set_parent(None)
                    if node.get_right() is not None:
                        node.get_right().set_parent(node)
                # Right-right rotation with node not as root
                else:
                    # Node is left child
                    if node.get_parent().get_left() is node:
                        node.get_parent().set_left(node.get_right())
                        node.set_right(node.get_parent().get_left().get_left())
                        node.get_parent().get_left().set_left(node)
                        node.get_parent().get_left().set_parent(node.get_parent())
                        node.set_parent(node.get_parent().get_left())
                        if node.get_right() is not None:
                            node.get_right().set_parent(node)
                    # Node is right child
                    else:
                        node.get_parent().set_right(node.get_right())
                        node.set_right(node.get_parent().get_right().get_left())
                        node.get_parent().get_right().set_left(node)
                        node.get_parent().get_right().set_parent(node.get_parent())
                        node.set_parent(node.get_parent().get_left())
                        if node.get_right() is not None:
                            node.get_right().set_parent(node)
                # Adjusts heights after right-right rotation
                if node.get_left() is None:
                    # Node is leaf is it has no right child after a left-left rotation
                    node.set_height(0)
                elif node.get_right() is None:
                    # Node height is one more than height of right node if there is no left node
                    node.set_height(node.get_left().get_height() + 1)
                else:
                    # Node height is one more than the greater of its childrens heights if both children exist
                    node.set_height(max(node.get_left().get_height(), node.get_right().get_height()) + 1)
            # Right-left rotation (double rotation)
            else:
                # First rotation
                node.set_right(node.get_right().get_left())
                node.get_right().get_parent().set_left(node.get_right().get_right())
                node.get_right().set_right(node.get_right().get_parent())
                node.get_right().get_right().set_parent(node.get_right())
                node.get_right().set_parent(node)
                if node.get_right().get_right().get_left() is not None:
                    node.get_right().get_right().get_left().set_parent(node.get_right().get_right())
                # Adjusts height of original right child after first rotation
                if node.get_right().get_right().get_left() is None and node.get_right().get_right().get_right() is not None:
                    # If only the right child exists, height is one more than the right child's
                    node.get_right().get_right().set_height(node.get_right().get_right().get_right().get_height() + 1)
                elif node.get_right().get_right().get_right() is None and node.get_right().get_right().get_left() is not None:
                    # If only the left child exists, height is one more than the left child's
                    node.get_right().get_right().set_height(node.get_right().get_right().get_left().get_height() + 1)
                elif node.get_right().get_right().get_left() is None and node.get_right().get_right().get_right() is None:
                    # If neither child exists, height is 0
                    node.get_right().get_right().set_height(0)
                else:
                    # If both children exist, height is one more than the greater of its children's heights
                    node.get_right().get_right().set_height(max(node.get_right().get_right().get_left().get_height(), node.get_right().get_right().get_right().get_height()))
                # Second rotation with node as root
                if node is self.root:
                    self.root = node.get_right()
                    node.set_right(self.root.get_left())
                    self.root.set_left(node)
                    node.set_parent(self.root)
                    self.root.set_parent(None)
                    if node.get_right() is not None:
                        node.get_right().set_parent(node)
                # Second rotation with node not as root
                else:
                    # Node is left child
                    if node.get_parent().get_left() is node:
                        node.get_parent().set_left(node.get_right())
                        node.set_right(node.get_parent().get_left().get_left())
                        node.get_parent().get_left().set_left(node)
                        node.get_parent().get_left().set_parent(node.get_parent())
                        node.set_parent(node.get_parent().get_left())
                        if node.get_right() is not None:
                            node.get_right().set_parent(node)
                    # Node is right child
                    else:
                        node.get_parent().set_right(node.get_right())
                        node.set_right(node.get_parent().get_right().get_left())
                        node.get_parent().get_right().set_left(node)
                        node.get_parent().get_right().set_parent(node.get_parent())
                        node.set_parent(node.get_parent().get_right())
                        if node.get_right() is not None:
                            node.get_right().set_parent(node)
                # Adjusts height of node after right-left rotation
                if node.get_left() is None and node.get_right() is not None:
                    # If only the right child exists, height is one more than the right child's
                    node.set_height(node.get_right().get_height() + 1)
                elif node.get_right() is None and node.get_left() is not None:
                    # If only the left child exists, height is one more than the left child's
                    node.set_height(node.get_left().get_height() + 1)
                elif node.get_right() is None and node.get_left() is None:
                    # If neither child exists, height is 0
                    node.set_height(0)
                else:
                    # If both children exist, height is one more than the greater of the children's heights
                    node.set_height(max(node.get_left().get_height(), node.get_right().get_height()))


class AVLNode: 

    def __init__ (self, val):
        # Raises TypeError if given value is not an int or float
        # Otherwise initializes instance value as given value
        if type(val) is int or type(val) is float:
            self.value = val
        else:
            raise TypeError("AVLNode value must be int or float")
        # Initializes children and parent as empty variables
        self.parent = None
        self.left = None
        self.right = None
        # Initializes height to be 0
        self.height = 0

    # Recursive method used to sort tree values by in-order traversal
    def recursive_sort (self, arr):
        if self.left is not None:
            self.left.recursive_sort(arr)
        arr.append(self.value)
        if self.right is not None:
            self.right.recursive_sort(arr)
        return arr

    # Recursive method used to draw the tree in the GUI
    def recursive_draw(self, x, y, lev, win):
        label = QLabel(format(self.value), win)
        label.move(x,y)
        label.setFont(QFont("Helvetica", 10))
        if self.left is not None:
            self.left.recursive_draw(int(round(x - (400 / (2**lev)))), y + 75, lev + 1, win)
        if self.right is not None:
            self.right.recursive_draw(int(round(x + (400 / (2**lev)))), y + 75, lev + 1, win)

    def get_value (self):
        return self.value

    def get_parent (self):
        return self.parent
    
    def get_left (self):
        return self.left

    def get_right (self):
        return self.right

    def get_height (self):
        return self.height

    def set_parent (self, node):
        self.parent = node

    def set_left (self, node):
        self.left = node

    def set_right (self, node):
        self.right = node

    def set_height (self, h):
        self.height = h

    def __str__ (self):
        return f"Value: {self.value}"


"""
Test Code
"""
t = AVLTree()
for i in range (30):
    t.add_node(i)
print(t.sort())
t.draw()