from tkinter import filedialog
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def whichfile():
    """
    Opens a Tkinter window for choosing a text file
    """
    # we don't want a full GUI, so keep the root window from appearing
    Tk().withdraw()

    # filetypes option restricts us to text files only
    filename = askopenfilename(filetypes=[("Txt files", "*.txt")])
    return filename


if __name__ == "__main__":
    whichfile()
