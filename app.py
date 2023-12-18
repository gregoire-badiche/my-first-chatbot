#!/usr/bin/env python3
# shebang !!

###########################
#                         #
#  app.py - Main program  #
#                         #
###########################

# Authors : Grégoire Badiche
#           Samy Gharnaout
#           Christine Khazzaka

from src.lib.features import features
from src.lib.response import most_relevant_document, get_phrase, pretty_response
from src.lib.ux import Scene
from src.lib.utils import list_files, ROOT
import src.lib.speeches as speeches
import src.lib.tfidf as tfidf

# Used to change character encoding on Windows
import os
# Used to detect CTRL+C hit, and terminal resize in UNIX
import signal
# Used for exit()
from sys import exit
# Used to detect which platform is used to ensure compatibility on Windows
# as signal.SIGWINCH doesn't exists on Windows, and we must set the
# terminal encoding with `chcp 65001`
from platform import system

# Changes the name of the window
print("\033]0;My first chatbot\007", end="")

scene = Scene()

# Function used to detect CTRL+C hits
def exit_handler(sig, _frame) -> None:
    signal.signal(sig, signal.SIG_IGN) # ignore additional signals
    scene.exit()
    exit(0)

# Registers the handler
signal.signal(signal.SIGINT, exit_handler)

# If the OS is UNIX based (based :P), registers a terminal resize handler
if(system() != "Windows"):
    signal.signal(signal.SIGWINCH, scene.update)
# If the OS is Windows, changes terminal encoding to better display characters
else:
    os.system("chcp 65001")

currenttheme = "presidents"
root = ROOT + '/cleaned/' + currenttheme
scores, idf = tfidf.tf_idf_from_dir(root)
# Alls the words across the documents of the current theme
words = scores.rows

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
    "change theme - Changes the current dicussion theme\n"
    "Anything else : discuss with the chatbot!\n")

def get_response(text:str) -> str|int:
    """
    Takes a question, and returns an anwser (prettied) to it
    May return:
        str - the actual response
        1 - no word latching the document
        2 - the highest TF-IDF score word isn't in the text with the most similarity
    """
    text = speeches.clean_text(text)
    text_vec = tfidf.term_frequency(text)
    text_mat = tfidf.tf_idf_score(text_vec, idf)
    mrd = most_relevant_document(scores, text_mat.reverse()[0], list_files(root, ".txt"))
    # If it has no most relevant document, e.g no words of the question matching the document
    if(mrd == 0):
        return 0
    else:
        isfound = False
        hsl = [] # highest scores list
        maxitems:int = len([i for i in range(len(text_mat.matrix)) if i > 0])
        while(not isfound):
            hs = "" # highest score index
            m = 0 # max
            s = text_mat.matrix # scores
            for i in range(len(s)):
                if(text_mat.rows[i] in hsl): continue
                if(s[i][0] > m):
                    m = s[i][0]
                    hs = text_mat.rows[i]
            hsl.append(hs)
            with open(f"{ROOT}/speeches/{currenttheme}/{mrd}", encoding='utf8') as fd:
                phrase = get_phrase(hs, fd.read())
            if(phrase):
                return phrase
            if(len(hsl) == maxitems):
                isfound = True
        return 1

while True:
    inpt = scene.handle()
    if(inpt == ""): continue
    choice = speeches.clean_text(inpt).strip()
    if(choice == "exit"):
        scene.exit()
        exit(0)
    
    # The choice is a feature
    if(choice in features.keys()):
        features[choice](scene)

    # Changes theme
    elif(choice == "change theme"):
        scene.new(
            "What do you want to talk about?\n"
            "1. Speeches by French presidents\n"
            "2. CLI articles on Wikipedia\n"
        )

        choices = {
            "1": "presidents",
            "2": "cli",
        }

        c = scene.handle()

        if(not c in choices.keys()):
            scene.new("This theme isn't valid.", error=True)
        
        currenttheme = choices[c]
        root = ROOT + '/cleaned/' + currenttheme
        scores, idf = tfidf.tf_idf_from_dir(root)
        words = scores.rows
        scene.new(f"Changed theme to {currenttheme}.")
    
    else:
        res = get_response(inpt)
        if(res not in [0, 1]):
            res = pretty_response(choice, res)
            scene.new(res)
        else:
            if(res == 1):
                scene.new("Unfortunately, I cannot provide an answer to this at the moment.", error=True)
            else:
                scene.new("I didn't understood. May you rephrase?", error=True)
