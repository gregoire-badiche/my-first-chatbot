############################################################
#                                                          #
#  features.py - Implementation of the features' functions #
#                                                          #
############################################################

# Authors : Grégoire Badiche
#           Samy Gharnaout
#           Christine Khazzaka

import src.lib.speeches as speeches
import src.lib.tfidf as tfidf
from src.lib.utils import ROOT, PRESIDENTS, list_files, lower, matrix
from src.lib.ux import Scene


root = 'src/cleaned/presidents'
scores, idf = tfidf.tf_idf_from_dir(root)
words = scores.rows

#1
def least_important_words(scores: matrix) -> list[str]:
    """Returns a list containing all the words with scores that are all 0"""

    # The list to be returned
    res = []

    s = scores.matrix
    words = scores.rows

    # For every word in the `scores`` matrix
    for i in range(len(s)):
        # If the sum of all the scores of the word is equal to 0 e.g all it scores are 0,
        # the word is added to the list
        if(sum(s[i]) == 0):
            res.append(words[i])
    
    return res

#2
def highest_score(scores:matrix) -> list[str]:
    """Returns a list containig all the words with the highest TF-IDF score"""

    # The list to be returned
    res = []
    # The max score
    highest = 0

    words = scores.rows
    scores = scores.matrix


    # For every word in the TF-IDF matrix
    for i in range(len(scores)):
        # For every score of this word
        for j in range(len(scores[i])):
            # If the score is equal to the highest, we add the word to the `res` list
            if(scores[i][j] == highest):
                res.append(words[i])
            # If the score is greater than the highest, deletes the values of the `res` list,
            # changes the highest variable and and adds the word to the empty list
            if(scores[i][j] > highest):
                highest = scores[i][j]
                res = []
                res.append(words[i])
    # Removes duplicates from the result
    return list(set(res))

#3
def most_repeated_word(name:str, scores:matrix, root:str) -> list[str]:
    """Returns a list containing all the most repeated words"""

    name = lower(name)

    words = scores.rows
    scores = scores.matrix

    # To get the most repeated word of a president, we can take all of his speeches, 
    # merge them all together and compute word frequency on the given text

    files = list_files(root, ".txt")
    # All the speeches of the given president, as his name should be in the files names
    filtered_files = [f for f in files if name in lower(f)]
    # The big merged text
    text = ""
    # We read and merge all texts
    for f in filtered_files:
        with open(f"{root}/{f}", "r") as t:
            text += t.read()
            text += " "
    # We remove last space added
    text = text[:-1]
    frequencies = tfidf.term_frequency(text)
    # And we compute the list of highest frequencies
    highest = 0
    res = []
    for k in frequencies.keys():
        # Excludes unimportants words
        if(sum(scores[words.index(k)]) == 0): continue
        if(frequencies[k] == highest):
            res.append(k)
        if(frequencies[k] > highest):
            highest = frequencies[k]
            res = [k]
    return res

#4
def who_spoke_of(word: str, root:str) -> tuple[set[str], str]:
    """Gives the set of president who spoke of a given word, and the one who talk about it the most"""

    files = list_files(root, ".txt")
    word = lower(word)
    plus = 0
    presidentplus = []
    presidents = set()
    for f in files:
        with open(f"{root}/{f}", "r") as t:
            text = t.read()
            frequencies = tfidf.term_frequency(text)
            if(word in frequencies.keys()):
                name = speeches.get_name(f)
                presidents.add(name)

                if(frequencies[word] == plus):
                    presidentplus.append(name)
                if(frequencies[word] > plus):
                    presidentplus = [name]
                    plus = frequencies[word]

    return ( presidents, presidentplus )

# 5
def who_spoke_first(words:list[str], operation: str, root:str) -> str:
    """
    Determine which president spoke first of the given words based on an operation.

    Parameters:
    - words (list[str]): A list of words.
    - operation (str): The logical operation to perform. Should be either "or" or "and".

    Returns:
    - str: The result indicating which president spoke first.
    """

    # The set of president who spoke of the given word
    pres = set()
    for w in words:
        # Here we get a set (and a string that we don't need)
        (p, _) = who_spoke_of(w, root)
        if(pres == set()):
            pres = p
        else:
            if(operation == "or"):
                pres = pres | p
            if(operation == "and"):
                pres = pres & p
    first_president = ""
    for p in PRESIDENTS:
        if p in pres:
            first_president = p
            break
    return first_president

# 6
def words_said_by_all(scores:matrix):
    """Determine the list of words said by all the presidents"""

    words = scores.rows
    scores = scores.matrix

    res = []
    for i in range(len(scores)):
        # Only scores with only 0 are said by all presidents, as in the TF-IDF formula IDF = log10(1) = 0
        if(sum(scores[i]) == 0):
            res.append(words[i])
    return res

# ---- Features implemetation ---- #

def feature3(scene:Scene):
    scene.new("Which president do you want the list of?")
    x = scene.handle()
    if(lower(x) in [lower(n) for n in PRESIDENTS]):
        scene.new("The list is :\n" + ", ".join(most_repeated_word(x, scores, root)))
    else:
        scene.new("I don't know this president. Please try again.", error=1)
    return

def feature4(scene:Scene):
    scene.new("Which word should we take?")
    x = scene.handle()
    if(lower(x) in words):
        scene.new(f"The presidents that talked about '{x}' are " + ", ".join(who_spoke_of(x, root)[0]))
    else:
        scene.new('None of the presidents ever talked about it', error=1)
    return

def feature5(scene:Scene):
    scene.new("What is the first word?")
    x = scene.handle()
    w1 = lower(x)
    if(w1 not in words):
        scene.new('None of the presidents ever talked about it', error=1)
        return
    scene.new("What is the second word?")
    x = scene.handle()
    w2 = lower(x)
    if(w2 not in words):
        scene.new('None of the presidents ever talked about it', error=1)
        return
    scene.new("What is the operation? Should be either 'and' or 'or'")
    x = scene.handle()
    # The mathematical operation asked
    op = lower(x)
    if(not op in ["and", "or"]):
        scene.new("This operation is unknown", error=1)
        return
    res = who_spoke_first([w1, w2], op, root)
    if(res):
        scene.new(f"The first president to talk about {w1} {op} {w2} is {res}")
    else:
        scene.new(f"None of the presidents ever talked about {w1} {op} {w2}")
    return

def featuretest(scene:Scene):
    # Wait...
    # Is that an...
    # EASTER EGG ⁉️⁉️
    # No way anyone would do this in a graded serious project
    # To test it, just type 'test'
    with open('src/lib/c3VwZXIgc2VjcmV0', "r", encoding="utf8") as fd:
        scene.new(fd.read(), _s=42)
    scene.new("schtroumpf chat")

# Returns a dict containing all the features, as it can now be dynamically called without a big if/elif/else
features = {
    "1": lambda scene: scene.new("The least important words are :\n" + ", ".join(least_important_words(scores))),
    "2": lambda scene: scene.new("The words with the highest scores are :\n" + ", ".join(highest_score(scores))),
    "3": feature3,
    "4": feature4,
    "5": feature5,
    "6": lambda scene: scene.new("The words said by all are :\n" + ", ".join(words_said_by_all(scores))),
    "test": featuretest
}
