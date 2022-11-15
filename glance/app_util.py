"""
Some utility functions
"""

import os
import re

import cv2


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
        # print(f"Available file type: {set(available_file_type)}")
        # return list(set(available_file_type))
        # return None
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


#================ CV2 ================
def get_haarcascade(model: str = None):
    """
    Get haarcascade model from opencv (cv2) data
    """
    default_face_model = "haarcascade_frontalface_default.xml"
    if model is None:
        model = default_face_model
    try:
        # Option 01: cv2  built-in method
        path = os.path.join(cv2.data.haarcascades, model)
        return cv2.CascadeClassifier(path)
    except:
        try:
            # Option 02: using `os` lib
            cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
            haar_model = os.path.join(cv2_base_dir, "data", model)
            return cv2.CascadeClassifier(haar_model)
        except:
            # Option 03: get from opencv github
            url = ("https://raw.githubusercontent.com/"
                   "opencv/opencv/master/data/haarcascades/"
                   "haarcascade_frontalface_default.xml")
            return cv2.CascadeClassifier(url)

def get_haarcascade_list():
    """
    Loop through the opencv (cv2) data to find haarcascade model
    """
    haar_list = []
    for file in os.listdir(cv2.data.haarcascades):
        if file.endswith(".xml"):
            haar_list.append(file)
    return haar_list


if __name__ == "__main__":
    pass

