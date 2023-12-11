################################################
#                                              #
#  speeches.py - Library used to handle texts  #
#                                              #
################################################

# re for RegEx
import os, re

# Used to remove directory with all it files
from shutil import rmtree as remove_folder

# Wrapper used to call the librairy as a main program
if(__name__ == "__main__"):
    from utils import ROOT, NAMES_PAIRS, LOWERCASE_LETTERS, lower
else:
    from src.lib.utils import NAMES_PAIRS, LOWERCASE_LETTERS, lower

def get_name(file_name: str) -> str:
    """Extracts the President's name from the file name"""

    # The RegEx with two match groups : ([A-Za-z ]+) and ([12]*).
    # Here the first match group will be used to extract the president name
    regex = r"Nomination_([A-Za-z ]+)([12]*)\.txt"

    # Matches the group matches
    matched = re.search(regex, file_name)

    # Did we actually got a match ?
    if(matched):
        # Takes the first group match : ([A-Za-z ]+)
        # Note : matched.group(0) returns the whole filename
        name = matched.group(1)
        return name
    else:
        # Raises an exception because the filename isn't valid
        raise ValueError("The name couldn't be matched")

def display_names(names: list[str]) -> None:
    """Displays the names of the presidents"""

    # For every names in the list
    for n in names:
        # Pretty cool format, uh ?
        # Output example : Jacques Chirac (as NAME_PAIRS[n] returns the firstname)
        print(f"{NAMES_PAIRS[n]} {n}")

def clean_text(text: str) -> str:
    """Cleans the text by lowercasing it and replacing any non-latin character or punctuation mark with spaces"""

    # The string to be returned
    cleaned_text = ""
    # The lowered text
    l_text = lower(text)

    # For every character in the lowered text
    for character in l_text:
        # Do we want to keep the character ?
        if(character in LOWERCASE_LETTERS):
            cleaned_text += character
        else:
            # Ensures that the text doesn't starts with a space
            if(len(cleaned_text) != 0):
                # If the previous character is not a space (to avoid multiple spaces)
                if(cleaned_text[-1] != " "):
                    cleaned_text += " "
    
    # Removes trailing space if it exists
    if(cleaned_text[-1] == " "):
        cleaned_text = cleaned_text[:-1]

    return cleaned_text

def convert_texts(files: list[str], root: str) -> None:
    """Cleans the texts and stores them into the `root/cleaned` directory"""

    # The directory at which the files should be stored
    # Not the cleanest way of doing it, but adding parameters is useless here
    directory = f"{root}/cleaned"

    # If the cleaned directory exists, removes it and all its content
    if os.path.exists(directory):
        remove_folder(directory)
    # And creates a brand new one !
    os.makedirs(directory)

    # For every file that should be cleaned (t stands for text)
    for t in files:
        # Opens and cleans the text
        with open(f"{root}/speeches/{t}", "r") as f_read:
            text = f_read.read()
            cleaned = clean_text(text)

            # And then writes it into a new file
            with open(f"{root}/cleaned/{t}", "w") as f_write:
                f_write.write(cleaned)

def tokenize(text:str) -> list[str]:
    return clean_text(text).split(' ')

# If the module is executed as a script, we automatically clean the texts
if(__name__ == "__main__"):
    import sys
    from utils import list_files
    files = list_files(f"{ROOT}/speeches", 'txt')
    convert_texts(files)
    print("Cleaned speeches")
    # I use zsh, and get triggered when the program don't exits with code 0
    sys.exit(0)
