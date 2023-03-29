import json, os

class Tierlist:
    def __init__(self, data = {"tiers": [], "author": "", "title": "", "order": ""}):
        self.data = data

    def author(self, name): 
        self.data["author"] = name
        return self

    def title(self, name): 
        self.data["title"] = name
        return self

    def from_file(self, path):
        if os.path.exists(path): 
            with open(path, "r") as f:
                self.data = json.load(f)
        else: self.data = {"tiers": [], "author": "", "title": "", "order": ""}

        return self

    def to_file(self, path):
        with open(path, "w") as f:
            f.write(json.dumps(self.data, indent=4))
        return self

    def get_order(self): 
        if len(self.data["order"]) == 0: return []
        return self.data["order"].split("|")

    def insert_order(self, name, index = None):
        orders = self.get_order()
        if index == None: index = len(orders)
        orders.insert(index, name)
        self.data["order"] = "|".join(orders)
        return self

    def remove_order(self, name, index = None):
        orders = self.get_order()
        if index == None: index = len(orders)
        orders.remove(name)
        self.data["order"] = "|".join(orders)
        return self

    def add_tier(self, name, index = None):
        if index == None: index = len(self.data["tiers"])
        self.data["tiers"].insert(index, {"name": name, "entries": []})
        self.insert_order(name, index)
        return self

    def remove_tier(self, name):
        for tier in self.data["tiers"]:
            if tier['name'] == name:
                self.data["tiers"].remove(tier)
                self.remove_order(name)
                break
        return self

    def get_tier(self, id_or_name):
        if type(id_or_name) == int or (type(id_or_name) == str and id_or_name.isdigit()):
            return self.data["tiers"][int(id_or_name)]

        id_or_name = str(id_or_name)

        for tierd in self.data["tiers"]:
            if tierd["name"].lower() == id_or_name.lower():        
                return tierd
                
        return None

    def remove_from_tier(self, tier, entry):
        if type(tier) == int or (type(tier) == str and tier.isdigit()):
            tier_index = int(tier)
            if entry in self.data["tiers"][tier_index]["entries"]:
                self.data["tiers"][tier_index]["entries"].remove(entry)
            return self

        tier = str(tier)

        for tierd in self.data["tiers"]:
            if tierd["name"].lower() == tier.lower(): 
                if entry in tierd['entries']:         
                    tierd["entries"].remove(entry)
        return self

    def add_to_tier(self, tier, entry):
        if type(tier) == int or (type(tier) == str and tier.isdigit()):
            tier_index = int(tier)
            if entry in self.data["tiers"][tier_index]["entries"]:
                self.data["tiers"][tier_index]["entries"].append(entry)
            return self

        tier = str(tier)

        for tierd in self.data["tiers"]:
            if tierd["name"].lower() == tier.lower():   
                if entry not in tierd['entries']:       
                    tierd["entries"].append(entry)
        return self


if __name__ == "__main__":
    tl = Tierlist()
    tl.add_tier("S").add_tier("A").add_tier("B").add_tier("C").add_tier("D")
    tl.add_to_tier("S", "Legends Arceus").add_to_tier(0, "Ultra Sun").add_to_tier("A", "HeartGold")
    print(tl.data)