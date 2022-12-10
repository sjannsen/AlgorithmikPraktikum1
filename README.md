# README ALGORITHMIK PRAKTIKUM 1

## Set up
- Download a collection of images (We used the collection of cats from "Cats vs Dogs", which can be found here: [Cats vs Dogs](https://www.microsoft.com/en-us/download/details.aspx?id=54765&utm_source=www.tensorflow.org&utm_medium=referral))
- Set up the collection of images in a folder. The project uses a folder called PetImages located in the source-directory
- If you want to use a different names or locate your images differently, set up the paths to the images:
    - Set up paths in main.py 
      - in line 16 `modul_name = "PetImages/Cat"`
      - in line 50 `image = get_image(Image.open('PetImages/Cat/8000.jpg'))`
    - Set up paths in AVLTree.py
      - in line - in line 16 `modul_name = "PetImages/Cat"`
    - Set up paths in AVLTreeTest.py
      - in line 18 `image_to_find_path = "PetImages/Cat/0.jpg"`
      - if you want to test with different images: in line 54 `image_to_find_path = "PetImages/Cat/0.jpg"` 
      - if you want to test with different images: in line 89 `image_to_find_path = "PetImages/Cat/0.jpg"`

## Testing
### For Testing Exercise 2
- If wanted, adjust/change images to test in main.py. See the section on [`Set up`](#set-up)
- Run main.py

### For Testing Exercise 3
- If wanted, adjust/change images to test in main.py See the section on [`Set up`](#set-up)
- Run AVLTreeTest.py

### For Testing Exercise 4
- In AVLTreeTest.py in line 18 `image_to_find_path = "PetImages/Cat/0.jpg"` link an image outside the collection <br> You can create a folder in the source-directory called TestImages, where you put other images outside the collection to test. If the image is called test0.jpg, you would have to adjust to: ``image_to_find_path = "TestImages/test0.jpg"``



## TODO
- [ ] Remove tests from AVLTree.py
- [ ] Directly implement tests for Exercise 4 
- [ ] Maybe solve problem of persistence by connecting to a database
- [ ] Rename main.py or rather outsource Exercise 2 to a new file 









