import os

# the `src` directory
ROOT = f"{os.path.dirname(os.path.realpath(__file__))}/.."

PRESIDENTS = [
    "Giscard dEstaing",
    "Mitterrand",
    "Chirac",
    "Sarcozy",
    "Hollande",
    "Macron",
]

def list_files(directory: str, extension: str) -> list[str]:
    """Lists all the files ending with `extension` in a given directory"""
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names
