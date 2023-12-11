#!/usr/bin/env python3

from src.lib.features import *
from src.lib.response import *
import src.lib.speeches as speeches
from src.lib.ux import Scene
import os

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

root = 'src/cleaned'
matrix, idf = tfidf.tf_idf_from_dir(root)
words = matrix.words()

scene.new("Hi!")
scene.new("Type 'exit' or hit CTRL+C at any time to exit gracefully")
scene.new("Which feature would you like to test today?")
scene.new(
    "1. Least important word\n"
    "2. Word with highest score\n"
    "3. Get the most repeated word from a president\n"
    "4. Get the list of president who spoke of a given word\n"
    "5. First president to talk about two words based on a set operation\n"
    "6. List of words said by all presidents\n"
    "Anything else : discuss with the chatbot!\n")

def feature3():
    scene.new("Which president do you want the list of?")
    x = scene.handle()
    if(lower(x) in [lower(n) for n in PRESIDENTS]):
        scene.new("The list is :\n" + ", ".join(most_repeated_word(x, matrix, root)))
    else:
        scene.new("I don't know this president. Please try again.", error=1)
    return

def feature4():
    scene.new("Which word should we take?")
    x = scene.handle()
    if(lower(x) in words):
        scene.new(f"The presidents that talked about '{x}' are " + ", ".join(who_spoke_of(x, root)[0]))
    else:
        scene.new('None of the presidents ever talked about it', error=1)
    return

def feature5():
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

def featuretest():
    with open('src/lib/c3VwZXIgc2VjcmV0', "r", encoding="utf8") as fd:
        scene.new(fd.read(), _s=42)
    scene.new("schtroumpf chat")

features = {
    "1": lambda: scene.new("The least important words are :\n" + ", ".join(least_important_words(matrix))),
    "2": lambda: scene.new("The words with the highest scores are :\n" + ", ".join(highest_score(matrix))),
    "3": feature3,
    "4": feature4,
    "5": feature5,
    "6": lambda: scene.new("The words said by all are :\n" + ", ".join(words_said_by_all(matrix))),
    "test": featuretest
}

def get_response(text:str) -> str:
    text = speeches.clean_text(text)
    text_vec = tfidf.term_frequency(text)
    text_mat = tfidf.tf_idf_score(text_vec, idf)
    mrd = most_relevant_document(matrix, text_mat.reverse()[0], list_files(root, ".txt"))
    if(mrd == 0):
        return False
    else:
        hs = "" # highest score index
        m = 0 # max
        s = text_mat.scores # scores
        for i in s:
            if(s[i][0] > m):
                m = s[i][0]
                hs = i
        with open(f"{root}/../speeches/{mrd}") as fd:
            phrase = get_phrase(hs, fd.read())
        return phrase

while True:
    inpt = scene.handle()
    choice = lower(inpt).strip()
    if(choice == "exit"):
        scene.exit()
        exit(0)
    
    if(choice in features.keys()):
        features[choice]()
    
    else:
        x = get_response(inpt)
        if(x):
            scene.new(x)
        else:
            scene.new("Je n'ai pas compris. Pouvez-vous reformuler ?", error=True)
