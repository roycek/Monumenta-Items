import tkinter as tk
from constants import Constants
import string


def returnstatcolor(stat, value):
    if ("cooldown" in stat) and ("reduction" not in stat) or ("requirement" in stat):
        return Constants.charmstatcolors["positiveCharm"] if value < 0 else Constants.charmstatcolors["negativeCharm"]
    else:
        return Constants.charmstatcolors["negativeCharm"] if value < 0 else Constants.charmstatcolors["positiveCharm"]


def charmtohumanreadable(stattext, statval):
    wordlist = " ".join([string.capwords(word) for word in stattext.split('_')
                         if word != "m" if word != "p" if word != "bow" if word != "tool"])
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

        tk.Label(charmframe, text=charm["name"],
                 font=("Helvetica", int(75 / len(statlist[0])),
                       ("bold", "underline") if charm["tier"] in ["Epic", "Legendary"] else "bold"),
                 bg="black", fg=charmnamecolor).grid(row=0, column=0, padx=2, pady=2, sticky="W")

        charmpowerframe = tk.Frame(charmframe, bg="black")
        charmpowerframe.grid(row=1, column=0, padx=2, pady=2, sticky="W")

        tk.Label(charmpowerframe, text="Charm Power: ", bg="black", fg=Constants.infotext).pack(side="left")
        for x in range(charm["power"]):
            tk.Label(charmpowerframe, text=u"\u2605", font=("Helvetica", 10), bg="black",
                     fg=Constants.masterworkstar).pack(side="left")
        tk.Label(charmpowerframe, text="-", bg="black", fg=Constants.infotext).pack(side="left")
        tk.Label(charmpowerframe, text=charm["class_name"], bg="black", fg=Constants.classcolors[charm["class_name"]])\
            .pack(side="left")

        for count, stat in enumerate(charm["stats"]):
            statvalue = charm["stats"][stat]

            tk.Label(charmframe, text=charmtohumanreadable(stat, statvalue),
                     font=("Helvetica", int(50 / len(statlist[0]))), bg="black", fg=returnstatcolor(stat, statvalue))\
                .grid(row=count+2, column=0, padx=2, pady=2, sticky="W")

        charmrarityframe = tk.Frame(charmframe, bg="black")
        charmrarityframe.grid(row=2+len(charm["stats"]), column=0, sticky="W")
        tk.Label(charmrarityframe, text="Ring", bg="black", fg=Constants.infotext).pack(side="left")

        if charm["tier"] == "Epic" or charm["tier"] == "Legendary":
            tk.Label(charmrarityframe, text=charm["tier"], bg="black", font=("Helvetica", 10, "bold"),
                     fg=Constants.tiercolors[charm["tier"].lower()]).pack(side="left")
        else:
            tk.Label(charmrarityframe, text=charm["tier"], bg="black",
                     fg=Constants.tiercolors[charm["tier"].lower()]).pack(side="left")

        tk.Label(charmframe, text=location, bg="black", fg=charmnamecolor).grid(row=3+len(charm["stats"]),
                                                                                column=0, sticky="W")
