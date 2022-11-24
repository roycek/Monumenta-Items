import tkinter as tk
from constants import Constants
import string


def charmtohumanreadable(stattext, statval):
    wordlist = " ".join([string.capwords(word) for word in stattext.split('_')])
    humanstr = ''

    if statval > 0:
        humanstr += '+'
    humanstr += str(statval)

    if "Percent" in wordlist:
        humanstr += "% "
    else:
        humanstr += " "

    wordlist = wordlist.replace(" Percent", "").replace(" Base", "").replace(" Flat", "")
    humanstr += wordlist

    return humanstr


def displaycharminfo(window, statlist):
    tk.Label(window, text="Charms", font=("Helvetica", 25, "bold"))\
        .grid(row=0, column=0, rowspan=3, columnspan=2, padx=20, pady=2, sticky="W")

    for index, charm in enumerate(statlist[0]):
        charmframe = tk.Frame(window, highlightbackground="blue", highlightthickness=3, bg="black")
        charmframe.grid(row=3, column=index, rowspan=6, padx=2, pady=2, sticky="N")

        location = charm["location"]
        charmnamecolor = Constants.locationcolors[location]

        tk.Label(charmframe, text=charm["name"], font=("Helvetica", int(75 / len(statlist[0])), "bold", "underline"),
                 bg="black", fg=charmnamecolor).grid(row=3, column=index, padx=20, pady=2)

        charmpowerframe = tk.Frame(charmframe, bg="black")
        charmpowerframe.grid(row=4, column=index, padx=2, pady=2)

        tk.Label(charmpowerframe, text="Charm Power: ", bg="black", fg=Constants.infotext).pack(side="left")
        for x in range(charm['power']):
            tk.Label(charmpowerframe, text=u"\u2605", font=("Helvetica", 10), bg="black",
                     fg=Constants.masterworkstar).pack(side="left")

        for count, stat in enumerate(charm["stats"]):
            statvalue = charm["stats"][stat]
            if "requirement" in stat:
                if statvalue < 0:
                    statcolor = Constants.charmstatcolors["positiveCharm"]
                else:
                    statcolor = Constants.charmstatcolors["negativeCharm"]
            elif ("cooldown" in stat) and ("reduction" not in stat):
                if statvalue < 0:
                    statcolor = Constants.charmstatcolors["positiveCharm"]
                else:
                    statcolor = Constants.charmstatcolors["negativeCharm"]
            else:
                if statvalue < 0:
                    statcolor = Constants.charmstatcolors["negativeCharm"]
                else:
                    statcolor = Constants.charmstatcolors["positiveCharm"]

            tk.Label(charmframe, text=charmtohumanreadable(stat, statvalue),
                     font=("Helvetica", int(50 / len(statlist[0]))), bg="black", fg=statcolor)\
                .grid(row=count+5, column=index, padx=20, pady=2)

        charmrarityframe = tk.Frame(charmframe, bg="black")
        charmrarityframe.grid(row=5+len(charm["stats"]), column=index)
        tk.Label(charmrarityframe, text="Ring", bg="black", fg=Constants.infotext).pack(side="left")

        if charm["tier"] == "Epic" or charm["tier"] == "Legendary":
            tk.Label(charmrarityframe, text=charm["tier"], bg="black", font=("Helvetica", 10, "bold"),
                     fg=Constants.tiercolors[charm["tier"].lower()]).pack(side="left")
        else:
            tk.Label(charmrarityframe, text=charm["tier"], bg="black",
                     fg=Constants.tiercolors[charm["tier"].lower()]).pack(side="left")

        tk.Label(charmframe, text=location, bg="black", fg=charmnamecolor).grid(row=6+len(charm["stats"]), column=index)
