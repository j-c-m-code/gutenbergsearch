from tkinter import filedialog
from tkinter import Tk


def whichdir():
    """
    Opens a Tkinter window for choosing a directory
    """
    root = Tk()
    root.directory = filedialog.askdirectory()
    root.destroy()  # closes the Tkinter window
    return root.directory


if __name__ == "__main__":
    whichdir()
