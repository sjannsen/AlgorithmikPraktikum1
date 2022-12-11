# Zum Einlesen der Pfade zu den jeweiligen Bildern
import os
from pathlib import Path
from typing import List

# Für Hashing
from PIL import Image
import imagehash

import time

# import mysql.connector
#
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root"
# )
#
# cursor = mydb.cursor()
#
# cursor.execute("CREATE DATABASE exercise1")
# cursor.execute("CREATE TABLE gfg (hash VARCHAR(255), path VARCHAR(255))")
# cursor.execute("SHOW DATABASE")
# for x in cursor:
#     print(x)

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


# setdefault()
# When the setdefault() method is called for a given key, it checks if the key exists in the dictionary.
# If the key does not exist, the setdefault() method creates the key and sets the default
# value (an empty list in this case) as the value for the key. If the key already exists, the setdefault() method
# returns the current value for the key. In either case, the append() method is used to add elements to the list
# associated with the key.


# list[[hash, path], [hash, path]...]
def get_image_hashes(list_of_all_image_paths):
    list_of_image_hashes_with_paths = {}
    for path in list_of_all_image_paths:
        original_hash = imagehash.dhash(Image.open(path))
        hash_as_string = str(original_hash)
        list_of_image_hashes_with_paths.setdefault(hash_as_string, []).append(path)
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

# Testing get_image() function

# First test
# Set start time before function
start_time = time.perf_counter()

image_paths_found = get_image(Image.open('PetImages/Cat/0.jpg'))

# Compute time passed while function call
elapsed_time = time.perf_counter() - start_time
print(f'Elapsed time while get_image(): {elapsed_time:.4f} seconds')

if image_paths_found == None:
    print("IMAGE NOT FOUND")
else:
    for path in image_paths_found:
        image_found = Image.open(path)
        image_found.show()
print("DONE")


# Second test
# Set start time before function
start_time = time.perf_counter()

image_paths_found = get_image(Image.open('PetImages/Cat/11000.jpg'))

# Compute time passed while function call
elapsed_time = time.perf_counter() - start_time
print(f'Elapsed time while get_image(): {elapsed_time:.4f} seconds')

if image_paths_found == None:
    print("IMAGE NOT FOUND")
else:
    for path in image_paths_found:
        image_found = Image.open(path)
        image_found.show()
print("DONE")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
