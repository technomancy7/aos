
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "quests",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            add
            ls
            complete
        """

    def new_quest(self, **data):
        quest = {
            "text": "",
            "exp": 0,
            "objectives": {},
            "id": "",
            "state": ""
        }
        quest.update(**data)
        return quest

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()

        match cmd:
            case "complete":
                d = ctx.get_data()
                if "." in ln:
                    questkey = ln.split(".")[0]
                    obj = ln.split(".")[1]
                    if d.get(questkey) and d[questkey]["objectives"].get(obj):
                        if d[questkey]["objectives"][obj]["state"] != "completed":
                            d[questkey]["objectives"][obj]["state"] = "completed"
                            #TODO exp rewards here
                            ctx.writeln(f"QUEST COMPLETED: {d[questkey]['text']}->{d[questkey]['objectives'][obj]['text']}")
                            ctx.save_data(d)
                        else:
                            ctx.writeln("Quest already completed.")
                    else:
                        ctx.writeln("Quest not found.")
                else:
                    if d.get(ln):
                        if d[ln]['state'] != "completed":
                            d[ln]['state'] = "completed"
                            ctx.writeln(f"QUEST COMPLETED: {d[ln]['text']}")

                        if len(d[ln]["objectives"]) > 0:
                            for obj, _ in d[ln]["objectives"].items():
                                if d[ln]["objectives"][obj]["state"] != "completed":
                                    d[ln]["objectives"][obj]["state"] = "completed"
                                    #TODO exp rewards here
                                    ctx.writeln(f"QUEST COMPLETED: {d[ln]['text']}->{d[ln]['objectives'][obj]['text']}")
                        #ctx.writeln(d[ln])
                        ctx.save_data(d)
                    else:
                        ctx.writeln("Quest not found.")

            case "ls":
                d = ctx.get_data()
                for _, quest in d.items():
                    if quest["state"] == "completed":
                        continue
                    text = f" # {quest['text']} ({quest['id']})"
                    if len(quest['objectives']) > 0:
                        text += "\n - Objectives: "
                        for _, item in quest['objectives'].items():
                            text += f"\n   * {item['text']} ({quest['id']}.{item['id']})"

                    ctx.write_panel(text)

            case "add":
                d = ctx.get_data()
                if ln == "":
                    quest_id = self.ctx.g.get_input("Quest unique ID:")
                    if d.get(quest_id):
                        return ctx.writeln("Quest ID already taken.")

                    quest_text = self.ctx.g.get_input("Quest text:")

                    ctx.writeln("If this is an objective under another quest, write its ID here.")
                    quest_parent = self.ctx.g.get_input("Quest parent ID:")
                    if quest_parent and not d.get(quest_parent):
                        return ctx.writeln("Parent not found.")

                    else:
                        if d[quest_parent]["objectives"].get(quest_id):
                            return ctx.writeln("Quest ID already taken.")

                    quest_exp = 0
                    if ctx.touch_config("quests.use_exp", False):
                        quest_exp = int(self.ctx.g.get_input("Quest reward EXP:")) or 0

                    q = self.new_quest(text=quest_text, id=quest_id, exp=quest_exp)

                    if quest_parent:
                        d[quest_parent]["objectives"][quest_id] = q
                        ctx.save_data(d)

                    else:
                        d[quest_id] = q
                        ctx.save_data(d)

                    ctx.writeln("Quest added.")

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
