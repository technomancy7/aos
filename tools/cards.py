from random import shuffle
import json

class CardManager:
    def __init__(self):
        self.defaults()

    def defaults(self):
        self.containers = {}
        self.active = None
        self.default_container = None

    def import_state(self, path):
        with open(path, "r") as f:
            js = json.load(f)
            self.containers = js['containers']
            self.active = js['active']

    def export_state(self, path):
        with open(path, "w+") as f:
            json.dump({
                "containers": self.containers,
                "active": self.active
            }, f)

    def discard_active(self):
        if self.active != None:
            self.containers["discard"].append(self.active)
            self.active = None

    def draw(self, target = None):
        self.discard_active()
            
        if target == None and self.default_container != None:
            target = self.default_container

        self.active = self.containers[target].pop()
        return self.active
    def new_container(self, tag):
        if not self.has_container(tag):
            self.containers[tag] = []

    def delete_container(self, tag):
        assert tag not in ["discard", "hand"], "Can't destroy discard or hand containers."

        if self.has_container(tag):
            oldc = self.get(tag)
            for card in oldc:
                self.get("discard").append(card)
            del self.containers[tag]

    def has_container(self, tag):
        return tag in list(self.containers.keys())

    def move(self, card_tag, container_from, container_to):#@todo move to/from active
        f = None
        if container_from != "active":
            f = self.get(container_from)

        t = None
        if container_to != "active": 
            t = self.get(container_to)

        for card in f:
            if card['name'] == card_tag: #@todo expand search
                if container_from != "active":
                    f.remove(card)
                else:
                    self.active = None

                if container_to != "active":    
                    t.append(card)
                else:
                    self.active = card

                return

    def shuffle(self, container):
        shuffle(self.get(container))

    def get(self, container):
        return self.containers.get(container, [])

    def new(self, *, jokers = 0, shuffle = False):
        self.defaults()

        self.new_container("basic")
        self.new_container("tarot")
        self.new_container("hand")
        self.new_container("discard")

        for suit in range(0, 4):
            suitname = [
                "clubs",
                "spades",
                "hearts",
                "diamonds"
            ][suit]
            suiticon = [
                "♣️",
                "♠️",
                "♥️",
                "♦️"
            ][suit]

            for value in range(1, 14):
                name = str(value)
                if value == 11: name = "jack"
                if value == 12: name = "queen"
                if value == 13: name = "king"
                if value == 1: name = "ace"

                nc = {
                    "value": value,
                    "name": f"{name} of {suitname}",
                    "suit": suitname,
                    "icon": suiticon
                }
                self.get("basic").append(nc)

        for suit in range(0, 4):
            suitname = [
                "wands",
                "swords",
                "cups",
                "pentacles"
            ][suit]

            for value in range(1, 15): #@todo higher arcanas
                name = str(value)
                if value == 11: name = "page"
                if value == 12: name = "knight"
                if value == 13: name = "queen"
                if value == 14: name = "king"
                if value == 1: name = "ace"

                nc = {
                    "value": value,
                    "name":  f"{name} of {suitname}",
                    "suit": suitname,
                    "icon": None
                }
                self.get("tarot").append(nc)
        
        tarot_higher_arcana = [
            "The Fool",
            "The Magician",
            "The High Priestess",
            "The Empress",
            "The Emperor",
            "The Hierophant",
            "The Lovers",
            "The Chariot",
            "Strength",
            "The Hermit",
            "Wheel of Fortune",
            "Justice",
            "The Hanged Man",
            "Death",
            "Temperance",
            "The Devil",
            "The Tower",
            "The Star",
            "The Moon",
            "The Sun",
            "Judgment",
            "The World"
        ]
        
        for i, ac in enumerate(tarot_higher_arcana):
            nc = {
                "value": i,
                "name":  f"{i} {ac}",
                "suit": None,
                "icon": None
            }
            self.get("tarot").append(nc)
    

        self.shuffle("basic")
        self.shuffle("tarot")

