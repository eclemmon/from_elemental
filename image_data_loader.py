from os import listdir
from os import path
import random

def get_image_paths(dir="./final_cells"):
    return [path.join(dir, img) for img in listdir(dir) if img.endswith(".png")]

def select_random_image(images):
    return random.choice(images)

def get_random_image_path():
    return select_random_image(get_image_paths())

if __name__ == "__main__":
    image_paths = get_image_paths()
    print(image_paths)
    # print(select_random_image(image_paths))