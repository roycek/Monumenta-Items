class EnabledBoxes:
    def __init__(self, selectedboxes):
        self.shielding = True if "Shielding" in selectedboxes else False
        self.poise = True if "Poise" in selectedboxes else False
        self.inure = True if "Inure" in selectedboxes else False
        self.steadfast = True if "Steadfast" in selectedboxes else False
        self.guard = True if "Guard" in selectedboxes else False
        self.secondwind = True if "SecondWind" in selectedboxes else False
        self.reflexes = True if "Reflexes" in selectedboxes else False
        self.evasion = True if "Evasion" in selectedboxes else False
        self.tempo = True if "Tempo" in selectedboxes else False
        self.cloaked = True if "Cloaked" in selectedboxes else False
        self.scout = True if "Scout" in selectedboxes else False
        self.cleridblessing = True if "ClericBlessing" in selectedboxes else False
        self.fol = True if "FOL" in selectedboxes else False
