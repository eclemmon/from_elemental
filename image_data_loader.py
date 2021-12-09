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
    """
    Gets a list of image paths
    :param dir: String as relative directory path
    :return: List of paths as strings
    """
    return [path.join(pathlib.Path(__file__).parent, dir, img) for img in
            listdir(path.join(pathlib.Path(__file__).parent, dir)) if img.endswith(".png")]

def select_random_image(images):
    """
    Selects a random image path from a list of images
    :param images: List of images
    :return: String of a path
    """
    return random.choice(images)

def get_random_image_path():
    """
    Helper function that calls get_image_paths() with the default relative path.
    :return: String of a path
    """
    return select_random_image(get_image_paths())

def get_image_names(dir="./violin_cells"):
    """
    Gets a list of the png files in a directory
    :param dir: String as relative directory path
    :return: List of png image file names
    """
    return [img for img in listdir(dir) if img.endswith(".png")]

def get_these_images(dir="./cello_cells", image_list=['cell_ether_ecl.png', 'cell_wind_ecl.png']):
    """
    Requests a particular set of files from (image files) from a relative directory path.
    :param dir: String as relative directory path
    :param image_list: List of file names.
    :return: List of full paths to file names.
    """
    result = []
    for img in image_list:
        if img in listdir(dir):
            result.append(path.join(dir, img))
    return result

def get_path_by_instrument_name(instrument_name):
    """
    Helper function to get full path to violin_cells/ directory or cello_cells/ directory
    :param instrument_name: String
    :return: String as path to violin or cello cells directories
    """
    sub_path = "{}_cells/".format(instrument_name)
    parent_path = pathlib.Path(__file__).parent
    instrument_path = path.join(parent_path, sub_path)
    return instrument_path

if __name__ == "__main__":
    image_paths = get_image_paths()
    print(image_paths)
    # print(select_random_image(image_paths))
    print(get_image_names())
    print(get_these_images())
    print(get_path_by_instrument_name("violin"))
    print(pathlib.Path(__file__).parent)