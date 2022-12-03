types = ["helmet", "chestplate", "leggings", "boots", "mainhand", "offhand"]


class Stats:
    def __init__(self, itemdata, formdata, enabledboxes):
        self.enabledBoxes = enabledboxes
        self.itemNames = {
            "helmet": formdata.helmet,
            "chestplate": formdata.chestplate,
            "leggings": formdata.leggings,
            "boots": formdata.boots,
            "mainhand": formdata.mainhand,
            "offhand": formdata.offhand
        }

        self.fullItemData = {}
        self.itemStats = {}
        for t in types:
            self.fullItemData[t] = itemdata[self.itemNames[t]] if self.itemNames[t] != '' else ''
            self.itemStats[t] = itemdata[self.itemNames[t]]["stats"] if self.itemNames[t] != '' else ''

        self.tenacity = formdata.tenacity
        self.vitality = formdata.vitality
        self.vigor = formdata.vigor
        self.focus = formdata.focus
        self.perspicacity = formdata.perspicacity

        self.currentHealthPercent = formdata.health / 100

