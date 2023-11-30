#############################################
#                                           #
#  utils.py - A collection of useful tools  #
#                                           #
#############################################

import os

# the `src` directory
ROOT = f"{os.path.dirname(os.path.realpath(__file__))}/.."

# The name, in chronological order, of all the presidents
PRESIDENTS = [
    "Giscard dEstaing",
    "Mitterrand",
    "Chirac",
    "Sarcozy",
    "Hollande",
    "Macron",
]

# The pairs used to associate a firstname with a name
NAMES_PAIRS = {
    "Chirac": "Jacques",
    "Giscard dEstaing": "Valéry",
    "Hollande": "François",
    "Mitterrand": "François",
    "Macron": "Emmanuel",
    "Sarkozy": "Nicolas",
}

LOWERCASE_LETTERS = "abcdefghijklmnopqrstuvwxyzüéâäåàçêëèïîìôöòûùÿáíóúñ"
UPPERCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÜÉÂÄÅÀÇÊËÈÏÎÌÔÖÒÛÙŸÁÍÓÚÑ"
# A dictionnary associating the uppercase letter with the lowercase one, used to lowercase
# simply the characters with accents, as they are spread in the ASCII table
DIC_UPPER_LOWER = {UPPERCASE_LETTERS[i]: LOWERCASE_LETTERS[i] for i in range(len(LOWERCASE_LETTERS))}

def list_files(directory: str, extension: str) -> list[str]:
    """Lists all the files ending with `extension` in a given directory"""
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def lower(text:str) -> str:
    res = ""
    for char in text:
        if(char in UPPERCASE_LETTERS):
            res += DIC_UPPER_LOWER[char]
        else:
            res += char
    return res
