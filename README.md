# my-first-chatbot

The Python Project at EFREI

## What is it about?

This Python program is designed to analyze a set of French presidential speeches at their nominations. It starts by extracting and associating president names with their first names, then displays the list of presidents. Subsequently, it cleans the speech texts by converting them to lowercase, removing punctuation, and saving the cleaned files in a new directory called “cleaned.” The program calculates the Term Frequency (TF) and Inverse Document Frequency (IDF) for each word, enabling the identification of least important words (with IDF scores of 0) and words with the highest TF-IDF scores. Additionally, it finds and displays the most repeated word(s) in for example, President Chirac’s speeches, identifies the president(s) who spoke most about a certain word and determines the first president to discuss for example “climat”. The program’s modular structure and diverse functionalities make it a comprehensive tool for extracting insights from the provided presidential speeches.

## How to install

Just download the code, no external dependencies are required

## How to run

just run the `app.py` file with `python app.py`

If you want to refresh the cleaned speeches, run the `src/lib/speeches.py` file

If you want to print the TF-IDF scores matrix, run the `src/lib/tfidf.py` file

By: 
- Grégoire BADICHE
- Samy GHARNAOUT
- Christine KHAZAKA
Class: L1-INT-4
