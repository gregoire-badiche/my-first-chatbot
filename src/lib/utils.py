import os, re
from shutil import rmtree as remove_folder

# the `src` directory
ROOT = f"{os.path.dirname(os.path.realpath(__file__))}/.."

def list_files(directory: str, extension: str) -> list[str]:
    """Lists all the files ending with `extension` in a given directory"""
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names
