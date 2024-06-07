
import time

class Scriptchi:
    def __init__(self, **d):
        self.name = d.get("name", "")
        self.hunger = d.get("hunger", 0)
        self.happiness = d.get("happiness", 0)
        self.tiredness = d.get("tiredness", 0)
        self.age = d.get("age", 0)
        self.alive = d.get("alive", True)

    def to_dict(self):
        return {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "tiredness": self.tiredness,
            "age": self.age,
            "alive": self.alive
        }

    def feed(self):
        self.hunger -= 1
        self.happiness += 1

    def play(self):
        self.happiness += 2
        self.tiredness += 1

    def sleep(self):
        self.tiredness -= 2

    def update(self):
        if self.alive:
            self.hunger += 1
            self.tiredness += 1
            self.age += 1

            if self.hunger >= 10 or self.tiredness >= 10:
                self.alive = False

            if self.happiness < 0:
                self.happiness = 0
            elif self.happiness > 10:
                self.happiness = 10

            if self.tiredness < 0:
                self.tiredness = 0
            elif self.tiredness > 10:
                self.tiredness = 10

            if self.hunger < 0:
                self.hunger = 0
            elif self.hunger > 10:
                self.hunger = 10

    def is_alive(self):
        return self.alive

    def get_hunger(self):
        return self.hunger

    def get_happiness(self):
        return self.happiness

    def get_tiredness(self):
        return self.tiredness

    def get_age(self):
        return self.age

    def __str__(self):
        if self.alive:
            return f"{self.name} (HU: {self.hunger}  HA: {self.happiness}  TI: {self.tiredness})"
        else:
            return f"{self.name} (DEAD)"


class Action:
    @staticmethod
    def __action__():
        return {
            "name": "scriptchi",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
        }

    def __help__(self, ctx):
        return """
            Default help.
        """

    def __run__(self, ctx):
        tg = Scriptchi(name = "Testy")

        print(tg.to_dict())
        #tg.rest()
        tg.update()
        print(tg.to_dict())
        clone = tg.to_dict()
        clone['name'] = "Clone"
        ctg = Scriptchi(**clone)
        print(ctg, ctg.to_dict())
        # Main functionality here.
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
