# my-first-chatbot

The Python Project at EFREI

## What is it about?

This Python program is designed to create a chatbot. We generate answers by making it analyze text files. We can then have a conversation with it about these texts. Subsequently, it cleans the speech texts by converting them to lowercase, removing punctuation, and saving the cleaned files in a new directory called “cleaned.” The program calculates the Term Frequency (TF) and Inverse Document Frequency (IDF) for each word, enabling the identification of least important words (with IDF scores of 0) and words with the highest TF-IDF scores.

## How to install

Just download the code, no external dependencies are required

## Files Descriptions

1. [features.py](./src/lib/features.py) useful to understand the CHATBOT FEATURES part
2. [response.py](./src/lib/response.py) used to generate responses
3. [speeches.py](./src/lib/speeches.py) used to handle the text documents
4. [tfidf.py](./source/lib/tfidf.py) all the functions that deal with tf_idf
5. [utils.py](./src/lib/utils.py) all the functions that are needed across files
6. [ux.py](./src/lib/ux.py) used to create the user interface
7. [app.py](./app.py) main program 

## How to run

Navigate the the folder containing the root folder, then depending on your OS:
- On UNIX, run the `app.py` file with `python app.py`
- On Windows, run the `app.py` file with `python3 app.py`

If you want to refresh the cleaned speeches, run the `src/lib/speeches.py` file

If you want to print the TF-IDF scores matrix, run the `src/lib/tfidf.py` file

By: 
- Grégoire BADICHE
- Samy GHARNAOUT
- Christine KHAZAKA
Class: L1-INT-4
