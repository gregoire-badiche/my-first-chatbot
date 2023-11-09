import math
if(__name__ == "__main__"):
    from utils import list_files
else:
    from src.lib.utils import list_files

def term_frequency(text: str) -> dict[str, int]:
    """Returns a dictionary associating with each word the number of times it appears in the string"""

    words = text.split(" ")
    res = {}

    for w in words:
        if(w in res.keys()):
            res[w] += 1
        else:
            res[w] = 1

    return res

def inverse_document_frequency(directory: str) -> dict[str: float]:
    """Returns a dictionary associating the IDF score with each word of each speech file in the directory"""

    files = list_files(directory, '.txt')
    res = {}

    for speech in files:
        words_in_file = []
        with open(f"{directory}/{speech}", "r") as fd:
            text = fd.read()
            words = text.split(" ")
            for w in words:
                if(w in res.keys()):
                    if(not w in words_in_file):
                        res[w] += 1
                        words_in_file.append(w)
                else:
                    res[w] = 1
                    words_in_file.append(w)
    
    for key in res.keys():
        res[key] = math.log(1 / res[key])
    
    return res

def tf_idf_score(directory: str) -> tuple[list[list[int]], list[str], list[str]]:
    """Computes the TF-IDF score"""

    itf = inverse_document_frequency(directory)
    files = list_files(directory, '.txt')

    scores = { k: [0] * len(files) for k in itf.keys() }

    for i in range(len(files)):
        speech = files[i]
        with open(f"{directory}/{speech}", "r") as fd:
            text = fd.read()
        frequencies = term_frequency(text)
        for k in frequencies.keys():
            scores[k][i] = frequencies[k] * itf[k]
    
    matrix = [scores[i] for i in scores.keys()]
    return (matrix, list(scores.keys()), files)

if(__name__ == "__main__"):
    print(tf_idf_score('./src/cleaned'))
