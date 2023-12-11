#############################################
#                                           #
#  utils.py - A collection of useful tools  #
#                                           #
#############################################

import os
from math import sqrt

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

class TF_IDF_Matrix:
    def __init__(self, scores:dict[dict[int]]) -> None:
        self.scores:dict[dict[int]] = scores
    
    def matrix(self):
        s = self.scores
        res = [[k for k in s[j]] for j in s]
        return res

    def words(self):
        return list(self.scores.keys())
    
    def files(self):
        return list(self.scores[self.words()[0]].keys())

    def getword(self, word) -> dict:
        if(not word in self.words()): raise IndexError()
        return self.scores[word]

    def getfile(self, file):
        if(not file in self.files()): raise IndexError()
        res = {}
        for k in self.words():
            res[k] = self.scores[k]
        return res
    
    def reverse(self) -> dict[str, dict]:
        res = {k: {j: self.scores[k][j] for j in self.scores[k]} for k in self.scores}
        return res
