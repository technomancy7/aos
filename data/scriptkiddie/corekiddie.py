class Corekid:
    def __init__(self, context):
        self.ctx = context
        self.inventory = {
            "food": 10
        }

        self.happiness = 50
        self.anger = 0
        self.energy = 100
        self.skill = 0
        self.money = 1000
        self.name = "Kid"

        self.born_on = 0
        self.last_interaction = ""
        self.last_interaction_on = 0

        self.memory = ["memory", "born_on", "last_interaction","last_interaction_on", "born_on", "happiness", "anger", "energy", "skill", "money", "name", "inventory"]

    #def __repr__(self):
        #return str(self.dump)

    def memorize(self, name):
        if name not in self.memory: self.memory.append(name)

    def forget(self, name):
        if name in self.memory: self.memory.remove(name)

    def output(self):
        out = {}
        for item in self.memory:
            out[item] = getattr(self, item)

        return out

    def save(self):
        kids = self.ctx.get_data()
        data = self.output()
        kids[self.name] = data
        self.ctx.save_data(kids)

    def load(self, name):
        kids = self.ctx.get_data()
        if kids.get(name):
            data = kids[name]
            for key in data["memory"]:
                setattr(self, key, data[key])

    def set_name(self, name): self.name = name

    def buy_food(self):
        #money down, food up
        pass

    def repeat_action(self, fn, times = 1):
        #do one of the function actions multiple times
        pass

    def train(self):
        #anger up, happiness down, energy down, skill up
        #fails if anger is over 100, happiness is under 0, or energy is under 0
        pass

    def feed(self):
        #energy up
        pass

    def play(self):
        #energy down, anger down, happiness up
        pass

    def hug(self):
        #anger down
        pass