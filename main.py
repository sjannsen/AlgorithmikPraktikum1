# Zum Einlesen der Pfade zu den jeweiligen Bildern
import os
from pathlib import Path
from typing import List

# Für Hashing
from PIL import Image
import imagehash


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


# list[[hash, path], [hash, path]...]
def get_image_hashes(list_of_all_image_paths):
    list_of_image_hashes_with_paths = {}
    for path in list_of_all_image_paths:
        original_hash = imagehash.dhash(Image.open(path))
        hash_as_string = str(original_hash)
        list_of_image_hashes_with_paths[hash_as_string] = path
    return list_of_image_hashes_with_paths


def get_image(image):
    original_hash = imagehash.dhash(image)
    hash_as_string = str(original_hash)
    if hash_as_string in list_of_images:
        return list_of_images[hash_as_string]
    else:
        return -1


list_of_paths = get_image_paths()
list_of_images = get_image_hashes(list_of_paths)

# Testing get() function
image = get_image(Image.open('PetImages/Cat/8000.jpg'))
if image == -1:
    print("IMAGE NOT FOUND")
else:
    image_found = Image.open(image)
    image_found.show()
print("DONE")

# TODO: Implement tests with images out of collection


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
