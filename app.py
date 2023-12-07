from src.lib.features import *
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