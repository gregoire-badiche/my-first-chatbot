import src.lib.speeches as speeches
import src.lib.tfidf as tfidf
from src.lib.utils import ROOT, PRESIDENTS, list_files

# Used for sys.extit()
import sys

(scores, words, files) = tfidf.tf_idf_score(f"{ROOT}/cleaned")

#1
def least_important_words() -> list[str]:
    """Returns a list containing all the words with scores that are all 0"""

    # The list to be returned
    res = []

    # For every word in the `scores`` matrix
    for i in range(len(scores)):
        # If the sum of all the scores of the word is equal to 0 e.g all it scores are 0,
        # the word is added to the list
        if(sum(scores[i]) == 0):
            res.append(words[i])
    
    return res

#2
def highest_score() -> list[str]:
    """Returns a list containig all the words with the highest TF-IDF score"""

    # The list to be returned
    res = []
    # The max score
    highest = 0

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
def most_repeated_word(name: str) -> list[str]:
    """Returns a list containing all the most repeated words"""

    name = name.lower()

    # To get the most repeated word of a president, we can take all of his speeches, 
    # merge them all together and compute word frequency on the given text

    files = list_files(f"{ROOT}/cleaned", ".txt")
    # All the speeches of the given president, as his name should be in the files names
    filtered_files = [f for f in files if name in f.lower()]
    # The big merged text
    text = ""
    # We read and merge all texts
    for f in filtered_files:
        with open(f"{ROOT}/cleaned/{f}", "r") as t:
            text += t.read()
            text += " "
    # We remove last space added
    text = text[:-1]
    frequencies = tfidf.term_frequency(text)
    # And we compute the list of highest frequencies
    highest = 0
    res = []
    for k in frequencies.keys():
        if(frequencies[k] == highest):
            res.append(k)
        if(frequencies[k] > highest):
            highest = frequencies[k]
            res = [k]
    return res

#4
def who_spoke_of(word: str) -> tuple[set[str], str]:
    """Gives the set of president who spoke of a given word, and the one who talk about it the most"""

    files = list_files(f"{ROOT}/cleaned", ".txt")
    word = word.lower()
    plus = 0
    presidentplus = []
    presidents = set()
    for f in files:
        with open(f"{ROOT}/cleaned/{f}", "r") as t:
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
def who_spoke_first(words: list[str], operation: str) -> str:
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
        # Here we get a set and a string that we don't need
        (p, _) = who_spoke_of(w)
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
def words_said_by_all():
    """Determine the list of words said by all the presidents"""
    res = []
    for i in range(len(scores)):
        s = 0
        for j in range(len(scores[i])):
            # The usage of `is` instead of `==` ensures that terms with scores equal to 0.0
            # are taken into account as terms with 0.0 appears in all speeches
            if(scores[i][j] is 0):
                s += 1
        if(s == len(scores[i])):
            res.append(words[i])
    return res

if(__name__ == "__main__"):
    print("1. Least important word")
    print("2. Word with highest score")
    print("3. Chirac's most repeated word")
    print("4. List of president who spoke of 'nation'")
    print("5. First president to talk about climat or nation")
    print("6. List of words said by all")
    choice = int(input("Choose your feature\n"))
    if(choice == 1):
        print(" ".join(least_important_words()))
    elif(choice == 2):
        print(" ".join(highest_score()))
    elif(choice == 3):
        print(" ".join(most_repeated_word("Chirac")))
    elif(choice == 4):
        print(" ".join(who_spoke_of("nation")))
    elif(choice == 5):
        print(who_spoke_first(["nation", "climat"], "or"))
    elif(choice == 6):
        print(" ".join(words_said_by_all()))
    else:
        print("Unknown feature")
        # Exit code 1 indicates an error (unknown feature)
        sys.exit(1)
    sys.exit(0)
