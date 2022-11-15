"""
USER
---

This module contains User class

Todo list:
- check if username in database
- load/save user
"""



import re
import json


def validate_username(username: str, minlen: int = 6) -> bool:
    """
    Validate username:
    
    - Must be start with `[a-zA-Z]`
    - Only contains alphabet and number
    - Must be larger than `minlen`
    """
    if minlen < 1:
        raise ValueError("minlen must be atleast 1")
    if len(username) < minlen:
        return False
    pattern = r"\b^[a-zA-Z]+[a-zA-Z0-9]*$\b"
    result = re.search(pattern, username)
    if result is None:
        return False
    return True


def export_to_json(data, location: str):
    """Export to JSON file format"""
    # dat = json.dumps(data, indent=4, sort_keys=True)
    dat = json.dumps(data)
    with open(location,"w") as json_file:
        json_file.writelines(dat)
    return None


class User:
    def __init__(self, username: str, first_name: str, last_name: str) -> None:
        self.username: str = username
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._balance: int = 0
        self.__account_password = None # Hidden, and remember to only store hash, salt

    def __str__(self):
        """String representative"""
        return f"Username: {self.username}\nName: {self._first_name} {self._last_name}\nBalance: {self._balance:,} VND"

    def update_balance(self, amount: int):
        assert type(amount) == int, "Value must be an int"
        self._balance += amount
    
    def export(self):
        """Export user data"""
        # return self.__dict__
        output = {
            "username": self.username,
            "fname": self._first_name,
            "lname": self._last_name,
            "balance": self._balance
        }
        return output



if __name__ == "__main__":
    pass