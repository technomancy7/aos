from tools.cards import CardManager
import os

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "cards",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
        }

    def __help__(self, ctx):
        return """
            draw <name>
                Draws a random card from deck named <name> and holds it in active slot.

            shuffle <name>
                Shuffles matching container.

            new <name>
                Creates a new hand called <name>
            
            delete <name>
                Deletes container and moves all cards in it to the Discard pile.
                Can't delete discard or hand.

            info/show
                If a card is held in active slot, shows it, plus basic info of each container.
                
            ls <optional tag>
                If tag given, list cards in matching container.
                Else, list all containers contents.

            move <target>
                moves card from active to container named <target>

            pull <container> <search>
                Pulls FIRST card matching pattern to active.
                Search will match against:
                    Value 
                    Name
                    Suit

            store/recall <name>
                Stores or recalls current deck/hand/active state

            reset
                Resets to blank state, using template

            escape
                While in interactive mode, run other AOS commands.

            explain
                Tries to explain current card using other AOS actions.
                Currently supports: tarot
        """

    def draw_random(self, deck = "basic"):
        self.cm = CardManager()
        self.cm.new()
        return self.cm.draw(deck)
        
    def __run__(self, ctx): 
        self.default_deck = ""
        self.cm = CardManager()
        #print(cm)
        cmd = ctx.get_string_ind(0)
        subcmd = []
        if len(ctx.get_string_list()) > 1:
            subcmd = ctx.get_string()[len(cmd)+1:].split(" ")
        print(cmd, subcmd)
        self.cm.new()
        """print(len(cm.get("basic")))
        print(len(cm.get("discard")))
        cm.draw("basic")
        print(cm.active)
        cm.draw("basic")
        print(cm.active)
        print(len(cm.get("basic")))
        print(cm.get("discard"))"""

        match cmd:
            case "interactive" | "i":
                ctx.writeln("Running card simulation using memory.")
                while True:
                    if self.default_deck:
                        i = input(f"[Cards:{self.default_deck}] > ")
                    else:
                        i = input("[Cards] > ")
                    cmd = i.split(" ")[0]
                    lna = i.split(" ")[1:]
                    
                    self.cardplayer(cmd, lna)
            
            case _:
                ctx.writeln("Running card simulation using live.json.")
                f = self.ctx.data_path()
                if not os.path.exists(f+"live.json"):
                    self.cm.export_state(f+"live.json")
                else:
                    self.cm.import_state(f+"live.json")
                self.cardplayer(cmd, subcmd)
                self.cm.export_state(f+"live.json")
        return ctx
    
    def cardplayer(self, cmd, lna):
        ln = " ".join(lna)
        cm = self.cm
        ctx = self.ctx
        match cmd:
            case "new":
                cm.new()
            case "create":
                cm.new_container(ln)
            case "destroy":
                try:
                    cm.delete_container(ln)
                except:
                    ctx.writeln("Can't destroy this container.")
            case "show" | "info" | "ls" | "list":
                if ln == "":
                    ctx.writeln(f"Holding: {cm.active}")
                    for container in cm.containers:
                        ctx.writeln(f"{container} {len(cm.containers[container])}")
                else:
                    cont = cm.get(ln)
                    for card in cont:
                        ctx.writeln(card)

            case "discard":
                if cm.active != None:
                    cm.discard_active()

            case "move":
                ctx.writeln(" | ".join([con for con in cm.containers.keys()]))
                fromc = input("From which container> ")
                c = cm.get(fromc)
                if len(c) > 0:
                    ctx.writeln(" | ".join([card['name'] for card in c]))
                    tomove = input("Card to move> ")
                    for card in cm.get(fromc):
                        if tomove == card["name"]: #@todo expand search
                            ctx.writeln(" | ".join([con for con in cm.containers.keys()]))
                            moveto = input("Move to where?> ")

                            cm.move(tomove, fromc, moveto)
                            ctx.writeln("Moved card.")
                            continue
                else:
                    ctx.writeln("Could not move card. Either container is empty or doesn't exist.")

            case "escape":
                ctx.quick_run(ln)

            case "store":
                if ln == "": ln = "default"
                dd = self.ctx.data_path()
                self.cm.export_state(dd+ln+".json")
                self.ctx.say(f"Stored current state to label {ln}.")

            case "recall":
                if ln == "": ln = "default"
                dd = self.ctx.data_path()
                self.cm.import_state(dd+ln+".json")
                self.ctx.say(f"Recalled stored state from label {ln}.")
            
            case "shuffle":
                if ln == "" and self.default_deck != "":
                    ln = self.default_deck

                if ln == "":
                    return ctx.say("No deck name given.")
                    
                self.default_deck = ln

                self.cm.shuffle(ln)

            case "draw":
                if ln == "" and self.default_deck != "":
                    ln = self.default_deck

                if ln == "":
                    return ctx.say("No deck name given.")
                self.default_deck = ln
                if cm.has_container(ln): 
                    ctx.writeln(f"Drawing from {ln}...")
                    cm.draw(ln)
                    ctx.say(f"You drew {cm.active['name']}!")

            case "explain":
                if ln == "" and self.default_deck != "":
                    ln = self.default_deck

                if ln == "":
                    return ctx.say("No deck name given.")
                    
                self.default_deck = ln

                if ln == "tarot":
                    ctx.quick_run(f"tarot i {cm.active['name']}")


    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

