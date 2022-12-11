# Zum Einlesen der Pfade zu den jeweiligen Bildern
import os
from pathlib import Path
from typing import List

# Für Hashing
import imagehash
from PIL import Image


def get_image_paths():
    # Project Location
    project_directory = os.path.dirname(os.path.realpath('__file__'))

    # Modul Location
    modul_name = "PetImages/Cat"

    path_to_file = os.path.join(project_directory, modul_name)
    list_of_all_image_paths: List = []

    for path in Path(path_to_file).rglob('*.jpg'):
        list_of_all_image_paths.append(os.path.join(path_to_file, path))

    return list_of_all_image_paths


def hash_image_to_key_with_difference_hash(path):
    original_hash = imagehash.dhash(Image.open(path))
    hash_as_string = str(original_hash)
    return hash_as_string


def hash_image_to_key_with_average_hash(path):
    original_hash = imagehash.average_hash(Image.open(path))
    hash_as_string = str(original_hash)
    return hash_as_string


def hash_image_to_key_with_perceptual_hash(path):
    original_hash = imagehash.phash(Image.open(path))
    hash_as_string = str(original_hash)
    return hash_as_string


def add_difference_hashed_images_to_tree(list_of_paths, avl_tree):
    for path in list_of_paths:
        avl_tree.insert(hash_image_to_key_with_difference_hash(path), path)


def add_average_hashed_images_to_tree(list_of_paths, avl_tree):
    for path in list_of_paths:
        avl_tree.insert(hash_image_to_key_with_average_hash(path), path)


def add_perceptual_hashed_images_to_tree(list_of_paths, avl_tree):
    for path in list_of_paths:
        avl_tree.insert(hash_image_to_key_with_perceptual_hash(path), path)


class AVLTree:
    def __init__(self):
        self.root = None

    def __repr__(self):
        if self.root == None: return ''
        content = '\n'  # to hold final string
        cur_nodes = [self.root]  # all nodes at current level
        cur_height = self.root.height  # height of nodes at current level
        sep = ' ' * (2 ** (cur_height - 1))  # variable sized separator between elements
        while True:
            cur_height += -1  # decrement current height
            if len(cur_nodes) == 0: break
            cur_row = ' '
            next_row = ''
            next_nodes = []

            if all(n is None for n in cur_nodes):
                break

            for n in cur_nodes:

                if n == None:
                    cur_row += '   ' + sep
                    next_row += '   ' + sep
                    next_nodes.extend([None, None])
                    continue

                if n.key != None:
                    buf = ' ' * int((5 - len(str(n.key))) / 2)
                    cur_row += '%s%s%s' % (buf, str(n.key), buf) + sep
                else:
                    cur_row += ' ' * 5 + sep

                if n.left_child != None:
                    next_nodes.append(n.left_child)
                    next_row += ' /' + sep
                else:
                    next_row += '  ' + sep
                    next_nodes.append(None)

                if n.right_child != None:
                    next_nodes.append(n.right_child)
                    next_row += '\ ' + sep
                else:
                    next_row += '  ' + sep
                    next_nodes.append(None)

            content += (cur_height * '   ' + cur_row + '\n' + cur_height * '   ' + next_row + '\n')
            cur_nodes = next_nodes
            sep = ' ' * int(len(sep) / 2)  # cut separator size in half
        return content

    def insert(self, key, pathToImage):
        """
        Insert a new node into the Tree. If the key already exists the associated Node will be updated.

        Return:
        -------
        If the Key does not exist return new Node.
        If the Key does exist return the Node that has been updated.
        """
        if self.root == None:
            newNode = self.createNewNode(key, pathToImage)
            self.root = newNode
            return newNode
        else:
            return self._insert(key, pathToImage, self.root)

    def _insert(self, key, pathToImage, cur_node):
        if key < cur_node.key:
            if cur_node.left_child == None:
                newNode = self.createNewNode(key, pathToImage)
                cur_node.left_child = newNode
                cur_node.left_child.parent = cur_node  # set parent
                self._inspect_insertion(cur_node.left_child)
                return newNode
            else:
                return self._insert(key, pathToImage, cur_node.left_child)
        elif key > cur_node.key:
            if cur_node.right_child == None:
                newNode = self.createNewNode(key, pathToImage)
                cur_node.right_child = newNode
                cur_node.right_child.parent = cur_node  # set parent
                self._inspect_insertion(cur_node.right_child)
                return newNode
            else:
                return self._insert(key, pathToImage, cur_node.right_child)
        elif key == cur_node.key:
            updatedNode = self.updateNode(cur_node, pathToImage)
            return updatedNode

    def print_tree(self):
        if self.root != None:
            self._print_tree(self.root)

    def _print_tree(self, cur_node):
        if cur_node != None:
            self._print_tree(cur_node.left_child)
            print('%s, h=%d' % (str(cur_node.key), cur_node.height))
            self._print_tree(cur_node.right_child)

    def height(self):
        if self.root != None:
            return self._height(self.root, 0)
        else:
            return 0

    def _height(self, cur_node, cur_height):
        if cur_node == None: return cur_height
        left_height = self._height(cur_node.left_child, cur_height + 1)
        right_height = self._height(cur_node.right_child, cur_height + 1)
        return max(left_height, right_height)

    def find(self, key):
        if self.root != None:
            return self._find(key, self.root)
        else:
            return None

    def _find(self, key, cur_node):
        if key == cur_node.key:
            return cur_node
        elif key < cur_node.key and cur_node.left_child != None:
            return self._find(key, cur_node.left_child)
        elif key > cur_node.key and cur_node.right_child != None:
            return self._find(key, cur_node.right_child)

    def find_most_similar(self, key):
        if self.root is not None:
            global most_similar_key
            global most_similar_node
            global hamming_distance

            most_similar_key = self.root.key
            hamming_distance = imagehash.hex_to_hash(self.root.key) - imagehash.hex_to_hash(key)
            most_similar_node = self.root

            self._find_most_similar(key, self.root)

            print("Hamming distance is: ")
            print(hamming_distance)

            if hamming_distance == 0:
                print("Images have the same hash and likely are very similar")
            elif 0 < hamming_distance < 10:
                print("Image is a potential variation")
            else:
                print("Likely a different image")

            return most_similar_node

        else:
            return None

    def _find_most_similar(self, key, cur_node):
        global most_similar_key
        global most_similar_node
        global hamming_distance

        if key == cur_node.key:
            return cur_node

        elif imagehash.hex_to_hash(cur_node.key) - imagehash.hex_to_hash(key) < \
                imagehash.hex_to_hash(most_similar_key) - imagehash.hex_to_hash(key):
            most_similar_key = cur_node.key
            most_similar_key = cur_node
            hamming_distance = imagehash.hex_to_hash(cur_node.key) - imagehash.hex_to_hash(key)

        if key < cur_node.key and cur_node.left_child is not None:
            if imagehash.hex_to_hash(cur_node.left_child.key) - imagehash.hex_to_hash(key) < \
                    imagehash.hex_to_hash(most_similar_key) - imagehash.hex_to_hash(key):
                most_similar_key = cur_node.left_child.key
                most_similar_node = cur_node.left_child
                hamming_distance = imagehash.hex_to_hash(cur_node.left_child.key) - imagehash.hex_to_hash(key)
            return self._find_most_similar(key, cur_node.left_child)

        elif key > cur_node.key and cur_node.right_child is not None:
            if imagehash.hex_to_hash(cur_node.right_child.key) - imagehash.hex_to_hash(key) < \
                    imagehash.hex_to_hash(most_similar_key) - imagehash.hex_to_hash(key):
                most_similar_key = cur_node.right_child.key
                most_similar_node = cur_node.right_child
                hamming_distance = imagehash.hex_to_hash(cur_node.right_child.key) - imagehash.hex_to_hash(key)
            return self._find_most_similar(key, cur_node.right_child)

    def delete_key(self, key):
        return self.delete_node(self.find(key))

    def delete_node(self, node):

        ## -----
        # Improvements since prior lesson

        # Protect against deleting a node not found in the tree
        if node == None or self.find(node.key) == None:
            print("Node to be deleted not found in the tree!")
            return None

        ## -----

        # returns the node with min key in tree rooted at input node
        def min_key_node(n):
            current = n
            while current.left_child != None:
                current = current.left_child
            return current

        # returns the number of children for the specified node
        def num_children(n):
            num_children = 0
            if n.left_child != None: num_children += 1
            if n.right_child != None: num_children += 1
            return num_children

        # get the parent of the node to be deleted
        node_parent = node.parent

        # get the number of children of the node to be deleted
        node_children = num_children(node)

        # break operation into different cases based on the
        # structure of the tree & node to be deleted

        # CASE 1 (node has no children)
        if node_children == 0:

            if node_parent != None:
                # remove reference to the node from the parent
                if node_parent.left_child == node:
                    node_parent.left_child = None
                else:
                    node_parent.right_child = None
            else:
                self.root = None

        # CASE 2 (node has a single child)
        if node_children == 1:

            # get the single child node
            if node.left_child != None:
                child = node.left_child
            else:
                child = node.right_child

            if node_parent != None:
                # replace the node to be deleted with its child
                if node_parent.left_child == node:
                    node_parent.left_child = child
                else:
                    node_parent.right_child = child
            else:
                self.root = child

            # correct the parent pointer in node
            child.parent = node_parent

        # CASE 3 (node has two children)
        if node_children == 2:
            # get the inorder successor of the deleted node
            successor = min_key_node(node.right_child)

            # copy the inorder successor's key to the node formerly
            # holding the key we wished to delete
            node.key = successor.key

            # delete the inorder successor now that it's key was
            # copied into the other node
            self.delete_node(successor)

            # exit function so we don't call the _inspect_deletion twice
            return

        if node_parent != None:
            # fix the height of the parent of current node
            node_parent.height = 1 + max(self.get_height(node_parent.left_child),
                                         self.get_height(node_parent.right_child))

            # begin to traverse back up the tree checking if there are
            # any sections which now invalidate the AVL balance rules
            self._inspect_deletion(node_parent)

    def search(self, key):
        if self.root != None:
            return self._search(key, self.root)
        else:
            return False

    def _search(self, key, cur_node):
        if key == cur_node.key:
            return True
        elif key < cur_node.key and cur_node.left_child != None:
            return self._search(key, cur_node.left_child)
        elif key > cur_node.key and cur_node.right_child != None:
            return self._search(key, cur_node.right_child)
        return False

    # Functions added for AVL...

    def _inspect_insertion(self, cur_node, path=[]):
        if cur_node.parent == None: return
        path = [cur_node] + path

        left_height = self.get_height(cur_node.parent.left_child)
        right_height = self.get_height(cur_node.parent.right_child)

        if abs(left_height - right_height) > 1:
            path = [cur_node.parent] + path
            self._rebalance_node(path[0], path[1], path[2])
            return

        new_height = 1 + cur_node.height
        if new_height > cur_node.parent.height:
            cur_node.parent.height = new_height

        self._inspect_insertion(cur_node.parent, path)

    def _inspect_deletion(self, cur_node):
        if cur_node == None: return

        left_height = self.get_height(cur_node.left_child)
        right_height = self.get_height(cur_node.right_child)

        if abs(left_height - right_height) > 1:
            y = self.taller_child(cur_node)
            x = self.taller_child(y)
            self._rebalance_node(cur_node, y, x)

        self._inspect_deletion(cur_node.parent)

    def _rebalance_node(self, z, y, x):
        if y == z.left_child and x == y.left_child:
            self._right_rotate(z)
        elif y == z.left_child and x == y.right_child:
            self._left_rotate(y)
            self._right_rotate(z)
        elif y == z.right_child and x == y.right_child:
            self._left_rotate(z)
        elif y == z.right_child and x == y.left_child:
            self._right_rotate(y)
            self._left_rotate(z)
        else:
            raise Exception('_rebalance_node: z,y,x node configuration not recognized!')

    def _right_rotate(self, z):
        sub_root = z.parent
        y = z.left_child
        t3 = y.right_child
        y.right_child = z
        z.parent = y
        z.left_child = t3
        if t3 != None: t3.parent = z
        y.parent = sub_root
        if y.parent == None:
            self.root = y
        else:
            if y.parent.left_child == z:
                y.parent.left_child = y
            else:
                y.parent.right_child = y
        z.height = 1 + max(self.get_height(z.left_child),
                           self.get_height(z.right_child))
        y.height = 1 + max(self.get_height(y.left_child),
                           self.get_height(y.right_child))

    def _left_rotate(self, z):
        sub_root = z.parent
        y = z.right_child
        t2 = y.left_child
        y.left_child = z
        z.parent = y
        z.right_child = t2
        if t2 != None: t2.parent = z
        y.parent = sub_root
        if y.parent == None:
            self.root = y
        else:
            if y.parent.left_child == z:
                y.parent.left_child = y
            else:
                y.parent.right_child = y
        z.height = 1 + max(self.get_height(z.left_child),
                           self.get_height(z.right_child))
        y.height = 1 + max(self.get_height(y.left_child),
                           self.get_height(y.right_child))

    def get_height(self, cur_node):
        if cur_node == None: return 0
        return cur_node.height

    def taller_child(self, cur_node):
        left = self.get_height(cur_node.left_child)
        right = self.get_height(cur_node.right_child)
        return cur_node.left_child if left >= right else cur_node.right_child

    def createNewNode(self, key, pathToImage):
        newNode = node(key)
        newNode.addPathToBucket(pathToImage)
        return newNode

    def updateNode(self, nodeToUpdate, pathToImage):
        nodeToUpdate.addPathToBucket(pathToImage)
        return nodeToUpdate


class node:
    def __init__(self, key=None):
        self.key = key
        self.pBucket: List = []  # Bucket of Paths (multiple Paths in a List)
        self.left_child = None
        self.right_child = None
        self.parent = None  # pointer to parent node in tree
        self.height = 1  # height of node in tree (max dist. to leaf) NEW FOR AVL

    def addPathToBucket(self, path: str):
        self.pBucket.append(path)

    def getPaths(self) -> List:
        return self.pBucket


# Testing

# dHash
print("Testing dHash")

# Setting up dHash AVL tree
d_hash_avl_tree = AVLTree()
add_difference_hashed_images_to_tree(get_image_paths(), d_hash_avl_tree)

# Test dHash AVL tree
image_to_find_path = "PetImages/Test/Yuumi_0.jpg"

# Test getImage()
image_found_with_get = d_hash_avl_tree.find(hash_image_to_key_with_difference_hash(image_to_find_path))
if image_found_with_get is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_get
    list_of_paths = node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()

# Test getMostSimilar()
image_found_with_most_similar = \
    d_hash_avl_tree.find_most_similar(hash_image_to_key_with_difference_hash(image_to_find_path))

if image_found_with_most_similar is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_most_similar

    list_of_paths = node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()


# averageHash
print("Testing averageHash")

# Setting up averageHash AVL tree
average_hash_avl_tree = AVLTree()
add_average_hashed_images_to_tree(get_image_paths(), average_hash_avl_tree)

# Test averageHash AVL tree
image_to_find_path = "PetImages/Test/Yuumi_0.jpg"

image_found_with_get = average_hash_avl_tree.find(hash_image_to_key_with_average_hash(image_to_find_path))
if image_found_with_get is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_get
    list_of_paths = node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()

# Test getMostSimilar()
image_found_with_most_similar = \
    average_hash_avl_tree.find_most_similar(hash_image_to_key_with_average_hash(image_to_find_path))

if image_found_with_most_similar is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_most_similar

    list_of_paths = node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()


# pHash
print("Testing pHash")

# Setting up pHash AVL tree
p_hash_avl_tree = AVLTree()
add_perceptual_hashed_images_to_tree(get_image_paths(), p_hash_avl_tree)

# Test pHash AVL tree
image_to_find_path = "PetImages/Test/Yuumi_0.jpg"

image_found_with_get = p_hash_avl_tree.find(hash_image_to_key_with_perceptual_hash(image_to_find_path))
if image_found_with_get is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_get
    list_of_paths = node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()

# Test getMostSimilar()
image_found_with_most_similar = \
    p_hash_avl_tree.find_most_similar(hash_image_to_key_with_perceptual_hash(image_to_find_path))

if image_found_with_most_similar is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_most_similar

    list_of_paths = node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()


# TODO: Persistence Problem: Connecting to database?

