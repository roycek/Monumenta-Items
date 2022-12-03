import tkinter as tk
from tkinter import messagebox as mbox
from ttkwidgets.autocomplete import AutocompleteCombobox
import json
import re

from utils.constants import Constants
from utils.getbuild import getitemstats
from utils.formdata import FormData
from utils.enabledboxes import EnabledBoxes

from tiles.charmtilegenerator import displaycharminfo
from tiles.geartilegenerator import displaygearinfo

from builder.stats import Stats

statlist = []
equipment = {}
charms = []

root = tk.Tk()
root.title("Monumenta Items")


class Gearinput:
    def __init__(self, window):
        self.window = window
        self.charminputfields = []
        self.charms = []
        self.gearinputfields = []
        self.masterworkinputfields = {}
        self.gear = [[], [], [], [], [], []]
        self.masterwork = {}

    def displaywidgets(self):
        self.charminputs()
        self.gearinputs()

        submitframe = tk.Frame(self.window)
        submitframe.grid(row=10, columnspan=10, pady=20)
        tk.Button(submitframe, text="Submit", font=("Helvetica", 25), command=lambda: self.getdata()) \
            .grid(row=0, column=0, padx=500)

    def getdata(self):
        for charminput in self.charminputfields:
            charm = charminput.get()
            if charm != '':
                self.charms.append(charm)

        for masterworkinput in self.masterworkinputfields:
            masterwork = self.masterworkinputfields[masterworkinput].get("1.0", "end-1c")
            self.masterwork[masterworkinput] = masterwork

        for index, gearinput in enumerate(self.gearinputfields):
            gear = gearinput.get()
            if gear != '':
                if self.masterwork[index] != '':
                    self.gear[index].append(f"{gear}-{self.masterwork[index]}")
                else:
                    self.gear[index].append(gear)

        self.displayequipmentinfo()

    def charminputs(self):
        tk.Label(self.window, text="Charms", font=("Helvetica", 25, "bold")) \
            .grid(row=0, column=0, rowspan=3, columnspan=2, padx=15, pady=2, sticky="W")
        tk.Label(self.window, text="Charms: ", font=("Helvetica", 15)).grid(row=3, column=0, sticky="E")
        charmrow = tk.Frame(self.window)
        charmrow.grid(row=3, column=1, sticky="W")
        for x in range(6):
            with open("utils/itemData.json", "r") as f:
                data = json.load(f)
                charmlist = []

                for item in data:
                    charmlist.append(item) if data[item]["type"] == "Charm" else None
                charmlist = list(charmlist)

                charminput = AutocompleteCombobox(charmrow, width=28)
                charminput.set_completion_list(charmlist)
                self.charminputfields.append(charminput)
                charminput.grid(row=0, column=x, padx=10, sticky="W")

    def gearinputs(self):
        tk.Label(self.window, text="Equipment", font=("Helvetica", 25, "bold")) \
            .grid(row=5, column=0, rowspan=3, columnspan=2, padx=15, pady=2, sticky="W")

        tk.Label(self.window, text="Gear: ", font=("Helvetica", 13)).grid(row=8, column=0, sticky="E")
        gearrow = tk.Frame(self.window)
        gearrow.grid(row=8, column=1, pady=5, sticky="W")
        tk.Label(self.window, text="Masterwork(if applicable): ", font=("Helvetica", 13)) \
            .grid(row=9, column=0, sticky="E")
        masterworkrow = tk.Frame(self.window)
        masterworkrow.grid(row=9, column=1, pady=5, sticky="W")

        for x in range(6):
            with open("utils/itemData.json", "r") as f:
                data = json.load(f)
                geartype = Constants.gearorder[str(x)]
                gearlist = []
                gearname = ''
                for item in data:
                    gearlist.append(item if data[item]["region"] not in "Architect's Ring" else re.sub(r"\d", "", item)
                                    .replace("-", " ").strip()) if data[item]["type"] in geartype else None
                    gearname = {0: "Helmet", 1: "Chestplate", 2: "Leggings", 3: "Boots", 4: "Mainhand", 5: "Offhand"}[x]
                gearlist = list(set(gearlist))

                gearinput = AutocompleteCombobox(gearrow, width=28)
                gearinput.set_completion_list(gearlist)
                self.gearinputfields.append(gearinput)
                tk.Label(gearrow, text=gearname).grid(row=0, column=x)
                gearinput.grid(row=1, column=x, padx=10)

            masterworkinput = tk.Text(masterworkrow, width=23, height=2)
            self.masterworkinputfields[x] = masterworkinput
            masterworkinput.grid(row=1, column=x, padx=11)

    def displayequipmentinfo(self):
        global statlist
        global charms
        global equipment

        equipment = {{0: "Helmet", 1: "Chestplate", 2: "Leggings", 3: "Boots", 4: "Mainhand", 5: "Offhand"}[x]: str
                     (piece) for x, piece in enumerate(self.gear)}
        charms = self.charms

        try:
            statlist = getitemstats(self.charms, [j for sub in self.gear for j in sub])
        except KeyError:
            mbox.showerror("Error", "Error searching API. "
                                    "Are you masterworking Valley and Isles gear? Check for spelling errors")
            return

        if statlist == [[], []]:
            mbox.showinfo("Empty Gear", "You did not enter any gear.")
            return

        for widget in self.window.winfo_children():
            widget.destroy()

        if len(statlist[0]) != 0:
            maincharmframe = tk.Frame(self.window)
            maincharmframe.grid(row=0, column=0, sticky="W")
            displaycharminfo(maincharmframe, statlist)

        if len(statlist[1]) != 0:
            maingearframe = tk.Frame(self.window)
            maingearframe.grid(row=1, column=0, sticky="W")
            displaygearinfo(maingearframe, statlist)

        tk.Button(self.window, text="Calculate Stats", command=lambda: setupbuilder(self.window)) \
            .grid(row=2, column=0, padx=500)


def setupbuilder(window):
    cbvarlist = [tk.BooleanVar() for _ in range(14)]
    cblist = []
    flist = []

    def getstats():
        with open("utils/itemData.json", "r") as f:
            _ = Stats(json.load(f), FormData(equipment, getentryvalues()), EnabledBoxes(getcheckboxvalues()))

    def getcheckboxvalues():
        selected = []
        for index, c in enumerate(cbvarlist):
            if c.get():
                selected.append(cblist[index].cget("text"))

        return selected

    def getentryvalues():
        texttype = {0: "Max Health Percent", 1: "Tenacity", 2: "Vitality", 3: "Vigor", 4: "Focus", 5: "Perspicacity"}
        output = {}
        for index, text in enumerate(flist):
            val = text.get("1.0", "end-1c")
            output[texttype[index]] = val

        return output

    for widget in window.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()

    checkboxframe = tk.Frame(window)
    checkboxframe.grid(row=2, column=0, columnspan=10, pady=10)

    for x in range(14):
        button = tk.Checkbutton(checkboxframe, text=Constants.situationals[x],
                                variable=cbvarlist[x], onvalue=True, offvalue=False)
        cblist.append(button)
        button.grid(row=0, column=x)

    infusionframe = tk.Frame(window)
    infusionframe.grid(row=3, columnspan=10, pady=10)

    for x in range(6):
        header = {0: "Max Health Percent", 1: "Tenacity", 2: "Vitality", 3: "Vigor", 4: "Focus", 5: "Perspiacity"}[x]
        tk.Label(infusionframe, text=header).grid(row=0, column=x, padx=50)
        inptext = tk.Text(infusionframe, width=15, height=1)
        flist.append(inptext)
        inptext.grid(row=1, column=x, padx=50)

    tk.Button(window, text="Calculate Stats", command=lambda: getstats()) \
        .grid(row=4, column=0, padx=630)


if __name__ == "__main__":
    Gearinput(root).displaywidgets()
    root.mainloop()
