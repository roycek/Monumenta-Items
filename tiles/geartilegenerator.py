import tkinter as tk
from utils.constants import Constants
import string


class StatFormatter:
    def __init__(self, stat, value):
        self.stat = stat
        self.value = value

    def tohumanreadable(self):
        humanstr = " ".join([string.capwords(word) for word in self.stat.split('_')
                             if word != "m" if word != "p" if word != "bow" if word != "tool"])\
            .replace("Prot", "Protection")\
            .replace("Protectionection", "Protection")\
            .replace("Regen", "Regeneration").replace("Jungle S Nourishment", "Jungle's Nourishment")

        stattype = ""
        for formats in Constants.statformats:
            if self.stat in formats:
                stattype = Constants.statformats[formats]

        match stattype:
            case "ENCHANT":
                humanstr = f"{humanstr} {self.value}"
            case "SINGLE_ENCHANT":
                pass
            case "ATTRIBUTE":
                humanstr = f"{'+' if self.value > 0 else ''}{self.value}" \
                           f"{'%' if 'Percent' in humanstr or 'Spell Power Base' in humanstr else ''} " \
                           f"{humanstr.replace(' Percent','').replace(' Base', '').replace(' Flat', '')}"
            case "CURSE":
                humanstr = f"Curse of {humanstr} {self.value}"
            case "SINGLE_CURSE":
                humanstr = f"Curse of {humanstr}" if humanstr != "Two Handed" else humanstr
            case "BASE_STAT":
                humanstr = f"{self.value} {humanstr.replace(' Base', '')}"

        return humanstr, stattype

    def statstyle(self):
        stattype = ""
        for formats in Constants.statformats:
            if self.stat in formats:
                stattype = Constants.statformats[formats]
        match stattype:
            case "ATTRIBUTE":
                if self.stat in ("armor", "agility"):
                    return "positiveDefence" if self.value > 0 else "negativeStat"
                else:
                    return "positiveStat" if self.value > 0 else "negativeStat"
            case "CURSE" | "SINGLE_CURSE":
                return "negativeStat"
            case "BASE_STAT":
                return "baseStat"
            case "ENCHANT" | "SINGLE_ENCHANT":
                return "enchant"

    def formatstat(self):
        return self.tohumanreadable()[0], self.tohumanreadable()[1], Constants.statcolors[self.statstyle()]


def statsorter(unformattedstats):
    newstatorder = [[], "negativeStat", [], "enchant", [], "baseStat", [], "positiveDefence", [],
                    "negativeStat", [], "positiveStat"]
    for (stat, stattype) in unformattedstats:
        match stattype:
            case "CURSE" | "SINGLE_CURSE":
                newstatorder[0].append(stat)
            case "ENCHANT" | "SINGLE_ENCHANT":
                newstatorder[2].append(stat)
            case "BASE_STAT":
                newstatorder[4].append(stat)

        match unformattedstats[(stat, stattype)]:
            case "#32cafc":
                newstatorder[6].append(stat)
            case "#fc5454":
                if stattype not in ("CURSE", "SINGLE_CURSE"):
                    newstatorder[8].append(stat)
            case "#5454fc":
                newstatorder[10].append(stat)

    orderedstats = {}
    for index, statgroup in enumerate(newstatorder):
        if not isinstance(statgroup, str):
            for stat in statgroup:
                orderedstats[stat] = Constants.statcolors[newstatorder[index + 1]]

    return orderedstats


def displaygearinfo(window, statlist):
    tk.Label(window, text="Equipment", font=("Helvetica", 25, "bold"))\
        .grid(row=0, column=0, rowspan=3, columnspan=2, padx=20, pady=2, sticky="W")

    for index, gearpiece in enumerate(statlist[1]):
        gearframe = tk.Frame(window, highlightbackground="blue", highlightthickness=3, bg="Black")
        gearframe.grid(row=3, column=index, rowspan=6, padx=5, pady=2, sticky="N")

        location = gearpiece["location"]
        gearnamecolor = Constants.locationcolors[location]

        tk.Label(gearframe, text=gearpiece["name"],
                 font=("Helvetica", 15,
                       ("bold", "underline") if gearpiece["tier"] in ["Epic", "Legendary"] else "bold"),
                 bg="black", fg=gearnamecolor).grid(row=0, column=0, padx=2, pady=2, sticky="W")
        tk.Label(gearframe, text=gearpiece["type"] + ' - ' + gearpiece["base_item"], bg="black", fg=Constants.infotext)\
            .grid(row=1, column=0, sticky="W")

        if gearpiece["region"] == "Ring" and gearpiece["tier"] \
                not in ["Tier 1", "Tier 2", "Tier 3", "Tier 4", "Tier 5"]:
            masterworkframe = tk.Frame(gearframe, bg="black")
            masterworkframe.grid(row=2, column=0, sticky="W")

            maxstars = {"Rare": 3, "Epic": 6}[gearpiece["tier"]]
            gearstars = gearpiece["masterwork"]

            tk.Label(masterworkframe, text="Masterwork: ", bg="black", fg=Constants.infotext).pack(side="left")
            for x in range(gearstars):
                tk.Label(masterworkframe, text=u"\u2605", font=("Helvetica", 10), bg="black",
                         fg=Constants.masterworkstar).pack(side="left")
            for x in range(maxstars-gearstars):
                tk.Label(masterworkframe, text=u"\u2606", font=("Helvetica", 10), bg="black", fg=Constants.infotext)\
                    .pack(side="left")

        unsortedstats = {}
        for count, stat in enumerate(gearpiece["stats"]):
            formattedstat, stattype, statcolor = StatFormatter(stat, gearpiece["stats"][stat]).formatstat()
            unsortedstats[(formattedstat, stattype)] = statcolor

        formattedstats = statsorter(unsortedstats)

        for count, formattedstat in enumerate(formattedstats):
            tk.Label(gearframe, text=formattedstat, bg="black", fg=formattedstats[formattedstat])\
                .grid(row=count+3, column=0, sticky="W")

        gearrarityframe = tk.Frame(gearframe, bg="black")
        gearrarityframe.grid(row=3+len(gearpiece["stats"]), column=0, sticky="W")
        tk.Label(gearrarityframe, text=gearpiece["region"], bg="black", fg=Constants.infotext).pack(side="left")

        if gearpiece["tier"] == "Epic" or gearpiece["tier"] == "Legendary":
            tk.Label(gearrarityframe, text=gearpiece["tier"], bg="black", font=("Helvetica", 10, "bold"),
                     fg=Constants.tiercolors[gearpiece["tier"].lower()]).pack(side="left")
        else:
            tk.Label(gearrarityframe, text=gearpiece["tier"], bg="black",
                     fg=Constants.tiercolors[gearpiece["tier"].lower()]).pack(side="left")

        tk.Label(gearframe, text=location, bg="black", fg=gearnamecolor).grid(row=4+len(gearpiece["stats"]),
                                                                              column=0, sticky="W")
