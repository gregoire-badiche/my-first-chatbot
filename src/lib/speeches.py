import os, re
from shutil import rmtree as remove_folder
if(__name__ == "__main__"):
    from utils import ROOT
else:
    from src.lib.utils import ROOT

def get_name(file_name: str) -> str:
    """Extracts the President's name from the file name"""

    regex = r"Nomination_([A-Za-z ]+)([12]*)\.txt"

    name = None
    matched = re.search(regex, file_name)
    if(matched):
        name = matched.group(1)
    
    return name

def display_names(names: list[str]) -> None:
    """Displays the names of the presidents"""

    NAMES_PAIRS = {
        "Chirac": "Jacques",
        "Giscard dEstaing": "Valéry",
        "Hollande": "François",
        "Mitterrand": "François",
        "Macron": "Emmanuel",
        "Sarkozy": "Nicolas",
    }

    for n in names:
        print(f"{NAMES_PAIRS[n]} {n}")

def clean_text(text: str) -> str:
    """Cleans the text by lowercasing it and replacing any non-latin character or punctuation mark with spaces"""

    LOWERCASE_LETTERS = "abcdefghijklmnopqrstuvwxyzüéâäåçêëèïîìôöòûùÿáíóúñ"

    cleaned_text = ""
    l_text = text.lower()

    for character in l_text:
        if(character in LOWERCASE_LETTERS):
            cleaned_text += character
        else:
            cleaned_text += " "
    
    # Removes double spaces
    cleaned_text = cleaned_text.split(" ")
    cleaned_text = filter(lambda x: bool(x), cleaned_text)
    cleaned_text = " ".join(cleaned_text)

    return cleaned_text

def convert_texts(files: list[str]) -> None:
    """Cleans the texts and stores them into the `src/cleaned` directory"""

    directory = f"{ROOT}/cleaned"
    if os.path.exists(directory):
        remove_folder(directory)
    os.makedirs(directory)

    for t in files:
        with open(f"{ROOT}/speeches/{t}", "r") as f_read:
            text = f_read.read()
            cleaned = clean_text(text)

            with open(f"{ROOT}/cleaned/{t}", "w") as f_write:
                f_write.write(cleaned)

if(__name__ == "__main__"):
    from src.lib.utils import list_files
    files = list_files(f"{ROOT}/speeches", 'txt')
    convert_texts(files)
    print("Cleaned speeches")
