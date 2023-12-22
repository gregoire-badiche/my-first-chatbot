#############################################
#                                           #
#  utils.py - A collection of useful tools  #
#                                           #
#############################################

# Author : Grégoire Badiche

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

LOWERCASE_LETTERS = "abcdefghijklmnopqrstuvwxyzüéâäåàçêëèïîìôöòûùÿáíóúñ0123456789"
UPPERCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÜÉÂÄÅÀÇÊËÈÏÎÌÔÖÒÛÙŸÁÍÓÚÑ0123456789"
# A dictionnary associating the uppercase letter with the lowercase one, used to lowercase
# easily the characters with accents, as they are spread in the ASCII table
DIC_UPPER_LOWER = {UPPERCASE_LETTERS[i]: LOWERCASE_LETTERS[i] for i in range(len(LOWERCASE_LETTERS))}

UNACCENT_K = "abcdefghijklmnopqrstuvwxyzüéâäåàçêëèïîìôöòûùÿáíóúñ0123456789"
UNACCENT_V = "abcdefghijklmnopqrstuvwxyzueaaaaceeeiiiooouuyaioun0123456789"
DIC_UNACCENT = {UNACCENT_K[i]: UNACCENT_V[i] for i in range(len(UNACCENT_K))}

QUESTION_STARTERS = {
    "comment": "Après analyse, ",
    "pourquoi": "Car, ",
    "peux tu": "Oui, bien sûr! Dans les faits, ",
    "quoi": "En ce qui concerne cela, ",
    "qui": "En termes de personnes, ",
    "quel": "Concernant ce choix, ",
    "est ce que": "Bien entendu, ",
    "penses tu que": "De mon point de vue, ",
    "explique": "Pour mieux comprendre, ",
    "decris": "En détail, ",
    "imagine": "En imaginant, ",
    "en quoi consiste": "En ce qui concerne cela, ",
}

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

def startwith(text:str, word:str) -> bool:
    """Check if a string starts with another string"""
    if(len(text) < len(word)): return False
    res = True
    for i in range(len(word)):
        if(word[i] != text[i]):
            res = False
            break
    return res

class matrix:
    """Generic matrix class used to type parameters, and handle matrix more easily"""
    matrix:list[list[float]]
    rows:list[str]
    cols:list[str]

    def __init__(self, matrix:list[list[float]], cols:list[str], rows:list[str]) -> None:
        self.matrix:list[list[float]] = matrix
        self.rows:list[str] = rows
        self.cols:list[str] = cols
    
    def reverse(self) -> dict[str, dict]:
        m = self.matrix
        res = [[] for i in range(len(m[0]))]
        for i in range(len(m)):
            for j in range(len(m[0])):
                res[j].append(m[i][j])
        return res
    
    def dict(self) -> dict:
        dict = {self.rows[i]: {self.cols: matrix[i][j] for j in range(len(matrix[i]))} for i in range(len(matrix))}
        return dict
