"""
Some utility functions
"""

import os
import re


#================ CONSTANT VARIABLES ================
IMG_TYPE = ("jpg", "png", "jpeg")
NP_DAT = "npy"

#================ PATH ================
def here_location():
    """Return current file location"""
    return os.path.abspath(os.path.dirname(__file__))

def location_wrap(file_location: str):
    """
    This function fix some `current working directory` error and return `abspath`
    """
    assert isinstance(file_location, str), "Must be a string"
    try: 
        here = here_location()
    except:
        here = ""
    return os.path.join(here, file_location)

def make_dir(*dir_name: str, loc_wrap: bool = True):
    """
    Create directory when not exist

    - `dir_name`: can use multiple str as child folder
    - `loc_wrap`: Use location_wrap

    Return `abspath`
    """
    path = os.path.join(*dir_name)
    if loc_wrap:
        if not os.path.exists(location_wrap(path)):
            os.makedirs(location_wrap(path))
            return os.path.abspath(location_wrap(path))
    else:
        if not os.path.exists(path):
            os.makedirs(path)
            return os.path.abspath(path)

def get_all_img_path(folder: str):
    """
    Return a list of tuple: (path to image file, filename/username)
    
    Outdated
    """
    image_pattern = r"\b^([\w ]+)([.]jpg|[.]png|[.]jpeg$)\b"
    imgs = []
    # for root, dirs, files in os.walk(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            result = re.search(image_pattern, file)
            if result is not None:
                imgs.append((os.path.join(root, file), result[1]))
    return imgs

def get_all_file_path(folder: str, *file_type: str):
    """
    Return a list of tuple: (path to choosen file type, filename/username)
    
    - `folder`: Folder path to search in
    - `file_type`: File type without the "." symbol. 
    Support multiple file type (separate with "," (coma))
    (Example: `jpg`, `png`, `npy`)
    """
    # Check file type
    # If no `file_type` entered then proceed to print available file type
    if len(file_type) < 1:
        available_file_type = []
        for _, _, files in os.walk(folder):
            for file in files:
                temp = re.search(r"\b.*[.](\w+$)\b", file)
                if temp is not None:
                    available_file_type.append(temp[1])
        raise ValueError(f"Available file type: {set(available_file_type)}")

    # Generate regex pattern
    temp_pattern = "|".join(f"[.]{x}" for x in file_type)
    pattern = f"\\b^([\w ]+)({temp_pattern}$)\\b"
    # print("Search pattern: ", pattern)
    
    # Iter through each folder to find file
    file_location = []
    # for root, dirs, files in os.walk(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            result = re.search(pattern, file)
            if result is not None:
                file_location.append((os.path.join(root, file), result[1]))
    return file_location



if __name__ == "__main__":
    pass

