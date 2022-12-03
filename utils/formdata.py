class FormData:
    def __init__(self, infodict, entrydict):
        def modifystr(s):
            return f"{s}".strip("[]").strip('"').strip("'")

        self.helmet = modifystr(infodict["Helmet"])
        self.chestplate = modifystr(infodict["Chestplate"])
        self.leggings = modifystr(infodict["Leggings"])
        self.boots = modifystr(infodict["Boots"])
        self.mainhand = modifystr(infodict["Mainhand"])
        self.offhand = modifystr(infodict["Offhand"])

        for x, entry in enumerate(entrydict):
            match entry:
                case "Max Health Percent":
                    self.health = int(entrydict[entry])
                case "Tenacity":
                    self.tenacity = int(entrydict[entry])
                    print(self.tenacity)
                case "Vitality":
                    self.vitality = int(entrydict[entry])
                case "Vigor":
                    self.vigor = int(entrydict[entry])
                case "Focus":
                    self.focus = int(entrydict[entry])
                case "Perspicacity":
                    self.perspicacity = int(entrydict[entry])
