###############################################################
#                                                             #
#  response.py - Library used to compute and parse responses  #
#                                                             #
###############################################################

# Authors : Grégoire Badiche
#           Samy Gharnaout

from math import sqrt
from src.lib.utils import matrix, startwith, lower, QUESTION_STARTERS
from src.lib.speeches import clean_text

def scalar_product(vector1: list[float], vector2: list[float]) -> int:
    """ Computes the scalar products of two vector of equal dimension """
    if(len(vector1) != len(vector2)):
        raise IndexError("Must be two vectors of equal length!")
    res = 0
    for i in range(len(vector1)):
        res += vector1[i] * vector2[i]
    return res

def vector_norm(vector: list[float]):
    """ Computes the norm of a vector """
    s = 0
    for v in vector:
        s += v ** 2
    return sqrt(s)

def similarity(vector1:list[float], vector2:list[float]) -> float:
    """ Computes similarity between to vectors """
    p1 = scalar_product(vector1, vector2)
    p2 = (vector_norm(vector1) * vector_norm(vector2))
    # If one or more of the vector is the null vector
    if(p2 == 0): return 0
    return p1 / p2

def most_relevant_document(mat:matrix, vector:list[float], document_names:list[str]) -> str:
    """ Computes the most relevant document from a TF_IDF matrix and a question TF_IDF vector """
    m = mat.reverse()
    maxs = 0
    doc = ""
    for i in range(len(m)):
        file = m[i]
        v = similarity(file, vector)
        if(v > maxs):
            maxs = v
            doc = document_names[i]
    return doc if maxs != 0 else 0

def get_phrase(word:str, raw_text:str) -> str:
    """ Returns the first phrase containing the word, in raw str, without the ending '.' """
    phrases = raw_text.split('.')
    phrases_cleaned = [clean_text(p) for p in phrases]
    res = [phrases[i] for i in range(len(phrases)) if word in phrases_cleaned[i].split(' ')]
    if(len(res)):
        return res[0]
    else:
        return False

def pretty_response(question:str, phrase:str) -> str:
    """ Adds a starter and provide punctuation to the answer provided """
    phrase = phrase.strip() + "."
    for key in QUESTION_STARTERS:
        if(startwith(question, key)):
            phrase = QUESTION_STARTERS[key] + lower(phrase[0]) + phrase[1:]
    return phrase
