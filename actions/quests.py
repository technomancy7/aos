
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
            add - Guided creation of a new quest
            ls - Shows current quests. Add -s to show completed.
            complete <quest_id> - Completes a quest
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
                            ctx.cexec("irlrpg", "give_exp", exp = d[questkey]["objectives"][obj]['exp'])
                            ctx.writeln(f"[green]QUEST COMPLETED[/green]: {d[questkey]['text']} -> {d[questkey]['objectives'][obj]['text']}")
                            ctx.save_data(d)
                        else:
                            ctx.writeln("Quest already completed.")
                    else:
                        ctx.writeln("Quest not found.")
                else:
                    if d.get(ln):
                        if d[ln]['state'] != "completed":
                            d[ln]['state'] = "completed"
                            ctx.cexec("irlrpg", "give_exp", exp = d[ln]['exp'])
                            ctx.writeln(f"[green]QUEST COMPLETED[/green]: {d[ln]['text']}")
                        else:
                            return ctx.writeln("Quest already completed.")

                        if len(d[ln]["objectives"]) > 0:
                            for obj, _ in d[ln]["objectives"].items():
                                if d[ln]["objectives"][obj]["state"] != "completed":
                                    d[ln]["objectives"][obj]["state"] = "completed"
                                    ctx.cexec("irlrpg", "give_exp", exp = d[ln]["objectives"][obj]['exp'])
                                    ctx.writeln(f"[green]QUEST COMPLETED[/green]: {d[ln]['text']} -> {d[ln]['objectives'][obj]['text']}")

                        ctx.save_data(d)
                    else:
                        ctx.writeln("Quest not found.")

            case "ls":
                d = ctx.get_data()
                show_completed = ctx.has_flag("s")
                q = 0
                for _, quest in d.items():
                    if quest["state"] == "completed" and not show_completed:
                        continue

                    q += 1
                    pre = "[blue]" if quest['state'] != "completed" else "[s]"
                    suf = "[/blue]" if quest['state'] != "completed" else "[/s]"
                    exp = ""
                    if ctx.touch_config("quests.use_exp", False) and quest['exp'] > 0:
                        exp = f" EXP: {quest['exp']} "

                    text = f" # {pre}{quest['text']}{suf} {exp}({quest['id']}) {quest['state']}"

                    if len(quest['objectives']) > 0:
                        text += "\n  - [green]Objectives[/green]: "
                        for _, item in quest['objectives'].items():
                            ipre = "[blue]" if item['state'] != "completed" else "[s]"
                            isuf = "[/blue]" if item['state'] != "completed" else "[/s]"
                            exp = ""
                            if ctx.touch_config("quests.use_exp", False) and item['exp'] > 0:
                                exp = f" EXP: {item['exp']} "
                            text += f"\n    * {ipre}{item['text']}{isuf} {exp}({quest['id']}.{item['id']}) {item['state']}"

                    ctx.write_panel(text)

                if q == 0:
                    ctx.writeln("No quests available.")

            case "add":
                d = ctx.get_data()
                if ln == "":
                    quest_id = self.ctx.g.get_input("Quest unique ID:")
                    if d.get(quest_id):
                        return ctx.writeln("Quest ID already taken.")

                    quest_text = self.ctx.g.get_input("Quest text:")

                    ctx.writeln("If this is an objective under another quest, write its ID here.")
                    quest_parent = self.ctx.g.get_input("Quest parent ID:")
                    if quest_parent != "":
                        if not d.get(quest_parent):
                            return ctx.writeln("Parent not found.")

                        else:
                            if d[quest_parent]["objectives"].get(quest_id):
                                return ctx.writeln("Quest ID already taken.")

                    quest_exp = 0
                    if ctx.touch_config("quests.use_exp", False):
                        e_gain = self.ctx.g.get_input("Quest reward EXP:")
                        if e_gain != "":
                            quest_exp = int(e_gain)
                            if quest_exp < 0: quest_exp = 0

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
