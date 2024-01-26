import random


class FoolsWorld:
    def __init__(self):
        self.level = 0
        self.player = {
            "health": 100,
            "money": 0,
            "energy": 100
        }
        self.higher_arcana = [
            "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
            "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
            "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
            "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgment", "The World"
        ]
        self.arcana = []
        for suit in range(0, 4):
            suitname = [ "wands", "swords", "cups", "pentacles" ][suit]

            for value in range(1, 15): 
                name = str(value)
                if value == 11: name = "page"
                if value == 12: name = "knight"
                if value == 13: name = "queen"
                if value == 14: name = "king"
                if value == 1: name = "ace"

                nc = {
                    "value": value, "name":  f"{name} of {suitname}", "suit": suitname, "icon": None
                }
                self.arcana.append(nc)
        random.shuffle(self.arcana)