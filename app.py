import src.lib.speeches as speeches
import src.lib.tfidf as tfidf
from src.lib.utils import ROOT

(scores, words, files) = tfidf.tf_idf_score(f"{ROOT}/cleaned")

least_important_words = []

for i in range(len(scores)):
    if(sum(scores[i]) == 0):
        least_important_words.append(words[i])

print(least_important_words)