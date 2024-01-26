import json

class Jade:
    def __init__(self):
        self.state = {}
        
    def new_zone(self, **obj):
        f = {
            "zone": True, 
            "object": False, 
            "contents": [],
            "exits": {
                "north": None,
                "south": None,
                "east": None,
                "west": None,
                "in": None,
                "out": None,
                "up": None,
                "down": None
            }
        }
        f.update(**obj)
        return f
    
    def new_object(self, **obj):
        f = {"object": True, "zone": False, "player": False, "count": 1, "contents": []}
        f.update(**obj)
        return f
    
    def new_exit(self, **obj):
        f = {"target": None, "locked": False}
        f.update(**obj)
        return f
    
    def new_state(self):
        self.state = {
            "name": "",
            "author": "",
            "version": 0,
            "variables": {},
            "world": [
                self.new_zone(name = "Intro", contents = [self.new_object(name="You", player=True)]),
                self.new_zone(name = "Outro"),
            ]
        }
        self.connect_zones("Intro", "north", "Outro")
        
    def locate(self, name):
        for zone in self.state["world"]:
            for ob in zone["contents"]:
                if self.check(ob["name"], name):
                    return (zone, ob)
                
    def check(self, search, target):
        """
        Check if the search term will match the target name
        """
        #TODO expand more methods, fuzzy
        if search.lower() == target.lower(): return True
        if target.lower().startswith(search.lower()): return True
        return False
    
    def invert_direction(self, d):
        dirs = {
            "north": "south",
            "east": "west",
            "up": "down",
            "in": "out"
        }
        
        for direc1, direc2 in dirs.items():
            if d == direc1: return direc2
            if d == direc2: return direc1
        
        return None
    
    def connect_zones(self, source, direction, target):
        inverted = self.invert_direction(direction)
        for zone in self.state["world"]:
            if self.check(zone["name"], source):
                if zone["exits"][direction] == None:
                    zone["exits"][direction] = self.new_exit(target = target)
                else:
                    zone["exits"][direction]["target"] = target
                    
            if self.check(zone["name"], target):
                if zone["exits"][inverted] == None:
                    zone["exits"][inverted] = self.new_exit(target = source)
                else:
                    zone["exits"][inverted]["target"] = target
    
s = Jade()
s.new_state()
#print(json.dumps(s.state, indent=4))
p = s.locate("You")
p[1]["tag"] = "LOL"
print(s.locate("You"))
