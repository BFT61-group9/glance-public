"""
Responsible for checking if encoded data exist
"""

# Import
import os
import json

import face_recognition
import numpy as np

from app_util import (
    location_wrap as locw,
    get_all_file_path, IMG_TYPE, NP_DAT
)



# START
path = locw("UserDB") # database path

def maintain(debug: bool = False):
    """
    Check each user in database:
    - If data is not encoded then proceed to encode
    - If data exist then continue
    """
    if debug: print("Getting data...")
    imgs = get_all_file_path(path, *IMG_TYPE)
    if debug: print("Done")

    if debug: print("Vadilating data...\n")
    for img in imgs:
        dir = os.path.dirname(img[0])

        # Check if encoded data exist
        if debug: print(f"Vadilating data for user: {img[1]}")
        data_path = os.path.join(dir, f"{img[1]}.{NP_DAT}")
        if os.path.exists(data_path):
            if debug: print("Data is healthy\n")
        else: # Encode datas
            if debug: print("No encoded data exist\nGenerating data...")
            know_image = face_recognition.load_image_file(img[0])
            encode = face_recognition.face_encodings(know_image)[0]
            np.save(data_path, encode)
            if debug: print("Data generated\n")
    return None

def load_data(folder: str):
    """Load data from database"""
    dat_path = get_all_file_path(folder, NP_DAT)
    final_data = [(np.load(dat[0]), dat[1]) for dat in dat_path]
    return final_data

def load_data_new(folder: str):
    """Load data (dict) from database"""
    dat_path = get_all_file_path(folder, NP_DAT)
    
    user_dat_path = get_all_file_path(folder, "json")
    if len(user_dat_path) < 1:
        raise FileNotFoundError
    else:
        udat = []
        for file in user_dat_path:
            with open(file[0]) as json_file:
                udat.append(json.load(json_file))
    
    # final_data = [(np.load(dat[0]), dat[1]) for dat in dat_path]
    final_data = []
    for i in range(len(dat_path)):
        final_data.append((np.load(dat_path[i][0]), dat_path[i][1], udat[i]))
    return final_data



if __name__ == "__main__":
    print(load_data_new(path)[0])