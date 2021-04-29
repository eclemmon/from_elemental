"""
Image Data Loader Module
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"


from os import listdir
from os import path
import random
import pathlib

def get_image_paths(dir="./final_cells"):
    return [path.join(pathlib.Path(__file__).parent, dir, img) for img in
            listdir(path.join(pathlib.Path(__file__).parent, dir)) if img.endswith(".png")]

def select_random_image(images):
    return random.choice(images)

def get_random_image_path():
    return select_random_image(get_image_paths())

def get_image_names(dir="./violin_cells"):
    return [img for img in listdir(dir) if img.endswith(".png")]

def get_these_images(dir="./cello_cells", image_list=['cell_ether_ecl.png', 'cell_wind_ecl.png']):
    result = []
    for img in image_list:
        if img in listdir(dir):
            result.append(path.join(dir, img))
    return result

def get_path_by_instrument_name(instrument_name):
    if instrument_name == "violin":
        instrument_path = pathlib.Path(__file__).parent
        instrument_path = path.join(instrument_path, "violin_cells/")
    else:
        instrument_path = pathlib.Path(__file__).parent
        instrument_path = path.join(instrument_path, "cello_cells/")
    return instrument_path

if __name__ == "__main__":
    image_paths = get_image_paths()
    print(image_paths)
    # print(select_random_image(image_paths))
    print(get_image_names())
    print(get_these_images())
    print(get_path_by_instrument_name("violin"))
    print(pathlib.Path(__file__).parent)