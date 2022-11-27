import tkinter as tk
from getbuild import getitemstats
from constants import Constants
from charmtilegenerator import displaycharminfo
from geartilegenerator import displaygearinfo

statlist = getitemstats(Constants.charms, Constants.gearr2)

root = tk.Tk()
root.title("Monumenta Items")


if __name__ == "__main__":
    maincharmframe = tk.Frame(root)
    maincharmframe.grid(row=0, column=0, sticky="W")
    displaycharminfo(maincharmframe, statlist)

    maingearframe = tk.Frame(root)
    maingearframe.grid(row=1, column=0, sticky="W")
    displaygearinfo(maingearframe, statlist)

    root.mainloop()
