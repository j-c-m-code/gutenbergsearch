"""
Opens a Tkinter window for choosing a file
Using currently to open Spacy docs from disk
"""
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def whichfile():
    """
    Opens a Tkinter window for choosing a file
    Using currently to open Spacy docs from disk
    """
    # we don't want a full GUI, so keep the root window from appearing
    Tk().withdraw()

    filename = askopenfilename()
    return filename


if __name__ == "__main__":
    whichfile()
