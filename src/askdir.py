"""
Opens a Tkinter window for choosing a directory
"""
from tkinter import Tk, filedialog


def whichdir():
    """
    Opens a Tkinter window for choosing a directory
    """
    root = Tk()
    # we don't want a full GUI, so keep the root window from appearing
    root.withdraw()
    directory = filedialog.askdirectory()
    return directory


if __name__ == "__main__":
    whichdir()
