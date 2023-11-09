import src.lib.speeches as speeches
import src.lib.tfidf as tfidf
from src.lib.utils import ROOT, PRESIDENTS, list_files

(scores, words, files) = tfidf.tf_idf_score(f"{ROOT}/cleaned")

def least_important_words():
    res = []
    for i in range(len(scores)):
        if(sum(scores[i]) == 0):
            res.append(words[i])
    
    return res

def highest_score():
    res = []
    highest = 0
    for i in range(len(scores)):
        for j in range(len(scores[i])):
            if(scores[i][j]):
                if(scores[i][j] == highest):
                    if(not(words[i] in res)):
                        res.append(words[i])
                if(scores[i][j] > highest or highest == 0):
                    highest = scores[i][j]
                    res = []
                    res.append(words[i])
    return res

def most_repeated_word(name):
    files = list_files(f"{ROOT}/cleaned", ".txt")
    filtered_files = [f for f in files if name in f]
    text = ""
    for f in filtered_files:
        with open(f"{ROOT}/cleaned/{f}", "r") as t:
            text += t.read()
            text += " "
    text = text[:-1]
    frequencies = tfidf.term_frequency(text)
    highest = 0
    res = []
    for k in frequencies.keys():
        if(frequencies[k] == highest):
            res.append(k)
        if(frequencies[k] > highest):
            highest = frequencies[k]
            res = [k]
    return res

# ----------- A REFAIRE

def who_spoke_of(word):
    files = list_files(f"{ROOT}/cleaned", ".txt")
    presidents = set()
    for f in files:
        with open(f"{ROOT}/cleaned/{f}", "r") as t:
            text = t.read()
            frequencies = tfidf.term_frequency(text)
            if(word in frequencies.keys()):
                name = speeches.get_name(f)
                presidents.add(name)
    first_president = ""
    for p in PRESIDENTS:
        if p in presidents:
            first_president = p
            break
    return (presidents, first_president)

def who_spoke_first(words, operation):
    pres = set()
    for w in words:
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

def words_sayed_by_all():
    res = []
    for i in range(len(scores)):
        s = 0
        for j in range(len(scores[i])):
            if(scores[i][j] != 0):
                s += 1
        if(s == len(scores[i])):
            res.append(words[i])
    return res

print(who_spoke_first(["climat", "écologie"], "and"))
