"""
Responsible to make user account
"""

# Import library
import os

import face_recognition
import cv2
import numpy as np

from app_util import (
    here_location as here, make_dir,
    location_wrap as locw
)
from user import User, validate_username, export_to_json


# START

# Init
path = locw("UserDB") # Path
make_dir(path) # Create UserDB folder if not exist
users_list = [dir for dir in os.listdir(path) if os.path.isdir(os.path.join(path, dir))] # generate list of current users
# print(users_list)
video_capture = cv2.VideoCapture(0) # Camera input


def _user_create(*overwrite: str) -> User:
    """
    Create User object [W.I.P]
    """

    while True:
        username = input("Enter username: ")
        if validate_username(username):
            if username not in users_list:
                break
            else:
                print("Username already exist!")
        else:
            print("Username must only include [a-zA-Z0-9]")

    first_name = input("Enter name: ")
    last_name = input("Enter last name: ")
    password = None # Soon

    return User(username, first_name, last_name)


def init_cam(auto: bool = False):
    """
    Camera capture start
    """
    # Create user
    user = _user_create()
    user.update_balance(500000) # Demo
    username = user.username
    userpath = make_dir(path, username)
    export_to_json(user.export(), os.path.join(userpath, f"{username}.json"))
    
    
    # Camera stuff
    vid_cam = cv2.VideoCapture(0)

    print("Press `f` to capture image")
    while (True):
        # Capture video frame
        _, image_frame = vid_cam.read()

        # Show cam
        cv2.imshow("User create (Press 'f' to capture and 'q' to exit)", image_frame)
        
        # Save img
        if cv2.waitKey(100) & 0xFF == ord("f"):
            try:
                print("Capturing image...")
                img_path = os.path.join(userpath, f"{username}.jpg")
                cv2.imwrite(img_path, image_frame)
                print("Image captured!")
                
                print("Encoding image...")
                print(f"Load image from {img_path}")
                loaded_img = face_recognition.load_image_file(img_path)
                # loaded_img = face_recognition.load_image_file(image_frame)
                encoded_img = face_recognition.face_encodings(loaded_img)[0]
                np.save(os.path.join(userpath, f"{username}.npy"), encoded_img)
                print("Image encoded!")
            except:
                print("Encode failed, recapturing...")
        # To stop taking video, press 'q' for at least 100ms
        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

    vid_cam.release()
    cv2.destroyAllWindows()



def main():
    init_cam()


if __name__ == "__main__":    
    main()