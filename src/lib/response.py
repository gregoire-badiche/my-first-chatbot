from math import sqrt
from src.lib.utils import TF_IDF_Matrix
from src.lib.speeches import clean_text

def scalar_product(vector1: list[int], vector2: list[int]) -> int:
    if(len(vector1) != len(vector2)):
        raise IndexError("Must be two vectors of equal length!")
    res = 0
    for i in range(len(vector1)):
        res += vector1[i] * vector2[i]
    return res

def vector_norm(vector: list[int]):
    s = 0
    for v in vector:
        s += v ** 2
    return sqrt(s)

def similarity(vector1:list[int], vector2:list[int]) -> int:
    return scalar_product(vector1, vector2) / (vector_norm(vector1) * vector_norm(vector2))

def most_relevant_document(matrix:TF_IDF_Matrix, vector:list[int]) -> str:
    m = matrix.reverse()
    maxs = 0
    doc = ""
    for file in m:
        if(not doc): doc = file
        v = similarity(file, vector)
        if(v > maxs):
            maxs = v
            doc = file
    return doc

def get_phrase(word:str, raw_text:str) -> str:
    phrases = raw_text.split('.')
    phrases = [clean_text(p) for p in phrases]
    phrase = [p for p in phrases if word in p][0]
    return phrase
