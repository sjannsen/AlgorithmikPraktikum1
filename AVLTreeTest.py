from tkinter import Image

import AVLTree
import importlib

importlib.import_module(AVLTree)

# Testing

# dHash
print("Testing dHash")

# Setting up dHash AVL tree
d_hash_avl_tree = AVLTree()
AVLTree.add_difference_hashed_images_to_tree(AVLTree.get_image_paths(), d_hash_avl_tree)

# Test dHash AVL tree
image_to_find_path = "PetImages/Cat/0.jpg"

# Test getImage()
image_found_with_get = d_hash_avl_tree.find(AVLTree.hash_image_to_key_with_difference_hash(image_to_find_path))
if image_found_with_get is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_get
    list_of_paths = AVLTree.node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()

# Test getMostSimilar()
image_found_with_most_similar = \
    d_hash_avl_tree.find_most_similar(AVLTree.hash_image_to_key_with_difference_hash(image_to_find_path))

if image_found_with_most_similar is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_most_similar

    list_of_paths = AVLTree.node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()


# averageHash
print("Testing averageHash")

# Setting up averageHash AVL tree
average_hash_avl_tree = AVLTree()
AVLTree.add_average_hashed_images_to_tree(AVLTree.get_image_paths(), average_hash_avl_tree)

# Test averageHash AVL tree
# image_to_find_path = "PetImages/Cat/0.jpg"

image_found_with_get = average_hash_avl_tree.find(AVLTree.hash_image_to_key_with_average_hash(image_to_find_path))
if image_found_with_get is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_get
    list_of_paths = AVLTree.node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()

# Test getMostSimilar()
image_found_with_most_similar = \
    average_hash_avl_tree.find_most_similar(AVLTree.hash_image_to_key_with_average_hash(image_to_find_path))

if image_found_with_most_similar is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_most_similar

    list_of_paths = AVLTree.node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()


# pHash
print("Testing pHash")

# Setting up pHash AVL tree
p_hash_avl_tree = AVLTree()
AVLTree.add_perceptual_hashed_images_to_tree(AVLTree.get_image_paths(), p_hash_avl_tree)

# Test pHash AVL tree
# image_to_find_path = "PetImages/Cat/0.jpg"

image_found_with_get = p_hash_avl_tree.find(AVLTree.hash_image_to_key_with_perceptual_hash(image_to_find_path))
if image_found_with_get is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_get
    list_of_paths = AVLTree.node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()

# Test getMostSimilar()
image_found_with_most_similar = \
    p_hash_avl_tree.find_most_similar(AVLTree.hash_image_to_key_with_perceptual_hash(image_to_find_path))

if image_found_with_most_similar is None:
    print("IMAGE NOT FOUND")
else:
    image_node = image_found_with_most_similar

    list_of_paths = AVLTree.node.getPaths(image_node)
    for image_path in list_of_paths:
        image_found_with_most_similar = Image.open(image_path)
        image_found_with_most_similar.show()

