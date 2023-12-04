#!/usr/bin/env python3

import src.lib.speeches as speeches
import src.lib.tfidf as tfidf
from src.lib.ux import Scene
from src.lib.utils import ROOT, PRESIDENTS, list_files, lower
import os 

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

    name = lower(name)

    # To get the most repeated word of a president, we can take all of his speeches, 
    # merge them all together and compute word frequency on the given text

    files = list_files(f"{ROOT}/cleaned", ".txt")
    # All the speeches of the given president, as his name should be in the files names
    filtered_files = [f for f in files if name in lower(f)]
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
        # Excludes unimportants words
        if(sum(scores[words.index(k)]) == 0): continue
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
    word = lower(word)
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
        # Only scores with only 0 are said by all presidents, as in the TF-IDF formula IDF = log10(1) = 0
        if(sum(scores[i]) == 0):
            res.append(words[i])
    return res

if(__name__ == "__main__"):
    # Used to detect CTRL+C hit and terminal resize in UNIX
    import signal
    # Used for exit()
    from sys import exit, stdout
    # Used to detect which platform is used to ensure compatibility on Windows
    # as signal.SIGWINCH doesn't exists on Windows, and we must set the
    # terminal encoding with `chcp 65001`
    from platform import system

    # Changes the name of the window
    stdout.write("\033]0;My first chatbot\007")

    scene = Scene()

    def exit_handler(sig, frame):
        signal.signal(sig, signal.SIG_IGN) # ignore additional signals
        scene.exit()
        exit(0)
    
    signal.signal(signal.SIGINT, exit_handler)
    if(system() != "Windows"):
        signal.signal(signal.SIGWINCH, scene.update)
    else:
        os.system("chcp 65001")


    scene.new("Hi!")
    scene.new("Type 'exit' or hit CTRL+C at any time to exit gracefully")
    scene.new("Which feature would you like to test today?")
    scene.new(
        "1. Least important word\n"
        "2. Word with highest score\n"
        "3. Get the most repeated word from a president\n"
        "4. Get the list of president who spoke of a given word\n"
        "5. First president to talk about two words based on a set operation\n"
        "6. List of words said by all presidents\n")
    while True:
        choice = scene.handle()
        if(choice == "exit"):
            scene.exit()
            exit(0)
        elif(lower(choice).strip() == "test"):
            with open('src/lib/c3VwZXIgc2VjcmV0', "r", encoding="utf8") as fd:
                scene.new(fd.read(), _s=42)
            scene.new("schtroumpf chat")
            continue
        else:
            try:
                choice = int(choice)
            except:
                choice = 7
        if(choice == 1):
            scene.new("The least important words are :\n" + ", ".join(least_important_words()))
        elif(choice == 2):
            scene.new("The words with the highest scores are :\n" + ", ".join(highest_score()))
        elif(choice == 3):
            scene.new("Which president do you want the list of?")
            x = scene.handle()
            if(lower(x) in [lower(n) for n in PRESIDENTS]):
                scene.new("The list is :\n" + ", ".join(most_repeated_word(x)))
            else:
                scene.new("I don't know this president. Please try again.", error=1)
        elif(choice == 4):
            scene.new("Which word should we take?")
            x = scene.handle()
            if(lower(x) in words):
                scene.new(f"The presidents that talked about {x} are " + ", ".join(who_spoke_of(x)[0]))
            else:
                scene.new('None of the presidents ever talked about it', error=1)
        elif(choice == 5):
            scene.new("What is the first word?")
            x = scene.handle()
            w1 = lower(x)
            if(w1 not in words):
                scene.new('None of the presidents ever talked about it', error=1)
                continue
            scene.new("What is the second word?")
            x = scene.handle()
            w2 = lower(x)
            if(w2 not in words):
                scene.new('None of the presidents ever talked about it', error=1)
                continue
            scene.new("What is the operation? Should be either 'and' or 'or'")
            x = scene.handle()
            op = lower(x)
            if(not op in ["and", "or"]):
                scene.new("This operation is unknown", error=1)
                continue
            res = who_spoke_first([w1, w2], op)
            if(res):
                scene.new(f"The first president to talk about {w1} {op} {w2} is {res}")
            else:
                scene.new(f"None of the presidents ever talked about {w1} {op} {w2}")
        elif(choice == 6):
            scene.new("The words said by all are :\n" + ", ".join(words_said_by_all()))
        else:
            scene.new("Unknown feature, please try again", error=1)
            
        scene.new("Which feature would you like to test?")
