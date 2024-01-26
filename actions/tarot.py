import json, random
from thefuzz import fuzz
from tools.cards import CardManager

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "tarot",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
        }

    def __extensions__(self):
        return [
            ["Tarot", None],
            ["Reading", None]
        ]
    def __help__(self, ctx):
        return """
            r | reading
            s | show | i | info
            ls

            Reading types (-r:<number>):
                1. single (Draws one card, to answer a single question)
                2. past, present, future (three cards, showing a moment of your past, how it effects you now, and how it will manifest in the future, or how you can overcome it)
                3. situation, action, outcome (three cards, a situation, something you can do, and how it may turn out)
                4. three options (think through a situation with 3 cards)

                Add -s:<name> flag to save reading under defined name.
        """

    def tarot(self):
        with open(self.ctx.aos_dir+"static_data/tarot.json") as f:
            return json.load(f)

    def draw_random(self):
        self.cm = CardManager()
        self.cm.new()
        return self.cm.draw("tarot")

    def get_card_info(self, name):
        highest_match = None
        highest_match_n = 0

        for card in self.data['cards']:
            m = fuzz.ratio(card['name'].lower(), name)
            m2 = fuzz.ratio(card['name_short'.lower()], name)
            if m > highest_match_n:
                highest_match = card
                highest_match_n = m

            if m2 > highest_match_n:
                highest_match = card
                highest_match_n = m

            if name == card['name_short']:
                highest_match = card
                highest_match_n = 100

            #if (len(line)> 4 and line in card['name'].lower()):
        return highest_match    
        #if highest_match != None:
            #card = highest_match   

    def __run__(self, ctx): 
        cmd = ctx.get_string_ind(0).lower()
        line = ""
        if len(ctx.get_string_list()) > 1:
            line = ctx.get_string()[len(cmd)+1:]

        line = line.lower()
        #print(cmd, "-", line)
        self.data = self.tarot()
        read_type = ctx.get_flag("t") or ctx.get_flag("r")
        save_reading = ctx.get_flag("s")
        match cmd:
            case "reading" | "r":
                cm = CardManager()
                cm.new()

                match read_type:
                    #@todo reading types
                    case "single" | "1":
                        card = cm.draw("tarot")
                        rev = random.choice([True, False])
                        info = self.get_card_info(card['name'])
                        ctx.writeln(f"{info['value']} - [red]{info['name']}[/red] ({info['name_short']})")
                        if not rev: ctx.writeln(f"[blue]Meaning[/blue]: {info['meaning_up']}")
                        if rev: ctx.writeln(f"[blue]Reversed[/blue]: {info['meaning_rev']}")
                        ctx.writeln(f"[blue]Description[/blue]: {info['desc']}")
                        if save_reading:
                            saved = {
                                "card": card,
                                "reversed": rev,
                                "meaning": info,
                                "label": save_reading
                            }
                            ctx.writeln(f"Will save {saved}")
                    case default:
                        ctx.writeln(f"Unknown reading type {read_type}")

            case "s" | "show" | "i" | "info":
                card = self.get_card_info(line)
                ctx.say(f"Here is information on {card['name']}.")
                ctx.writeln(f"{card['value']} - [red]{card['name']}[/red] ({card['name_short']})")
                ctx.writeln(f"[blue]Meaning[/blue]: {card['meaning_up']}")
                ctx.writeln(f"[blue]Reversed[/blue]: {card['meaning_rev']}")
                ctx.writeln(f"[blue]Description[/blue]: {card['desc']}")

            case "list" | "ls":
                for card in self.data['cards']:
                    ctx.writeln(f"{card['name']} ({card['name_short']})")
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

