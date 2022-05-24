
from re import M

class PYMCommands:
    @staticmethod
    def extend(state):
        state.register_command("echo", PYMCommands._echo)

    @staticmethod
    def _echo(state, line):
        state.log(line)

class PYM:
    @staticmethod
    def default_object(**opt):
        f = {
            "id": "",
            "name": "",
            "description": "",
            "tags": [],
            "contains": [],
            "container": "",
            "object_type": "entity"
        }
        f.update(**opt)
        return f

    def __init__(self):
        self.objects = [
            PYM.default_object(id = "player", container = "start", name = "Player"),
            PYM.default_object(id = "start", object_type = "zone", contains=["player"])
        ]
        self.variables = {}
        self.commands = {}
        self.events = {} 
        PYMCommands.extend(self)
        self.buffer = []
        self.alive = False

    def load(self, path): pass 
    def save(self, path): pass
       
    def on(self, name, fn): self.events[name] = fn

    def emit(self, event_name, **opts):
        f = self.events.get(event_name, None)
        if f: f(state = self, **opts)

    def register_command(self, name, fn): 
        self.commands[name] = fn

    def execute(self, command, line):
        f = self.commands.get(command, None)
        if f: f(self, line)

    def log(self, line, source = "log"): self.buffer.append({"source": source, "line": line})
    def purge_log(self): self.buffer.clear()

    def readline(self, line): pass #main entry point for text input
    def entity(self, e): pass #resolve input as an entity, if its a dict return it, if string, search tag
    def zone(self, z): pass


    def move_entity(self, ent, new_zone): pass
    def locate(self, ent): pass # return zone of entity
    def player(self): return self.get(id = "player")
    def location(self): return None #get players location as object
    def current(self): return self.player(), self.location()


    def setv(self, key, v):
        self.variables[key] = v
    
    def getv(self, key, d = None):
        return self.variables.get(key, d)


    def get(self, **opt):
        for obj in self.objects:
            for key in opt.keys():
                if obj.get(key) == opt.get(key):
                    return obj

    def get_match(self, **opt):
        for obj in self.objects:
            good = True
            for key in opt.keys():
                if obj.get(key) != opt.get(key):
                    good = False
            if good: return obj

    def find(self, **opt):
        out = []
        for obj in self.objects:
            for key in opt.keys():
                if obj.get(key) == opt.get(key):
                    out.append(obj)
        return out

    def find_match(self, **opt):
        out = []
        for obj in self.objects:
            good = True
            for key in opt.keys():
                if obj.get(key) != opt.get(key):
                    good = False
            if good: out.append(obj)
        return out