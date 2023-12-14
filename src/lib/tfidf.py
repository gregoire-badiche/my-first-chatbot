#####################################################
#                                                   #
#  tfidf.py - Library used to compute TF-IDF score  #
#                                                   #
#####################################################

import math

# Wrapper used to call the librairy as a main program
if(__name__ == "__main__"):
    from utils import list_files
else:
    from src.lib.utils import list_files, matrix

def term_frequency(text: str) -> dict[str, int]:
    """Returns a dictionary associating with each word the number of times it appears in the string"""

    # Transforms the text into an array of words
    words = text.split(" ")
    # The variable that will be returned
    res = {}

    # For every word
    for w in words:
        # Is the word already in the result dictionnary ?
        if(w in res.keys()):
            # We add 1 to its count
            res[w] += 1
        else:
            # We initialize its count at 1
            res[w] = 1

    return res

def inverse_document_frequency(directory: str) -> dict[str: float]:
    """Returns a dictionary associating the IDF score with each word of each speech file in the directory"""

    # Lists all the files in the document
    files = list_files(directory, '.txt')
    # The variable that will be returned 🤯🤯🤯
    res = {}

    # For every cleaned text
    for speech in files:
        # Opens it with a nice format string
        # fd stands for file descriptor
        with open(f"{directory}/{speech}", "r") as fd:
            text = fd.read()
            # `words`` stores the set of all the words of the text
            list_words = text.split(" ")
            words = set(list_words)

            # For every word
            for w in words:
                # If the word have already been encountered in another text
                if(w in res.keys()):
                    # We increment the counter by one
                    res[w] += 1
                # If it is the first time the word is seen, initializes its counter
                else:
                    res[w] = 1
    
    # Applies the formula for every word
    for key in res.keys():
        res[key] = math.log10(len(files) / res[key])
    
    return res

def tf_idf_score(tf_vector:dict[int], idf_vector:dict[int]) -> matrix:
    mat = {k:[0] for k in idf_vector.keys()}
    for word in tf_vector.keys():
        if(word not in idf_vector.keys()): continue
        mat[word] = [tf_vector[word] * idf_vector[word]]
    mat = [mat[k] for k in mat.keys()]
    return matrix(mat, ["1"], list(idf_vector.keys()))

def tf_idf_from_dir(directory: str) -> tuple[matrix, list]: 
    """Computes the TF-IDF score"""

    # Gets the idf dictionnary
    idf = inverse_document_frequency(directory)
    files = list_files(directory, '.txt')

    # Initialization of the scores dictionnary, with each word of the document bein associated a value of 0
    # This dictionnary will be put into a matrix and returned
    # The returned dict looks like
    # {
    #   "word_1": [score_text_1, score_text_2, score_text_3, ...],
    #   "word_2": [score_text_1, score_text_2, score_text_3, ...],
    #    ...
    # }
    # and the dict here looks like
    # {
    #   "word_1": [0, 0, 0, ...],
    #   "word_2": [0, 0, 0, ...],
    #    ...
    # }
    scores = { k: [0] * len(files) for k in idf.keys() }

    # For every speech file
    for i in range(len(files)):
        speech = files[i]

        # Opens the file, read it, and compute the TF score
        with open(f"{directory}/{speech}", "r") as fd:
            text = fd.read()
        frequencies = term_frequency(text)

        # Then computes the TF-IDF score for every word of the text, and writes it into the variable
        # For every word of the text
        for k in frequencies.keys():
            scores[k][i] = frequencies[k] * idf[k]

    # Transfoms the dict into a matrix
    res = [scores[i] for i in scores.keys()]

    # Returns the matrix as a matrix object
    return matrix(res, files, list(idf.keys())), idf

# If the module is called as a program
if(__name__ == "__main__"):
    import sys
    print(tf_idf_score('./src/cleaned'))
    # I use zsh, and get triggered when the program don't exits with code 0
    sys.exit(0)
