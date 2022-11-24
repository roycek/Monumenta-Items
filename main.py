import tkinter as tk
from getbuild import getitemstats
from constants import Constants
from charmtilegenerator import displaycharminfo

statlist = getitemstats(Constants.charms, Constants.gear)

root = tk.Tk()
root.title("Monumenta Items")
root.columnconfigure(6)


if __name__ == "__main__":
    displaycharminfo(root, statlist)
    root.mainloop()
