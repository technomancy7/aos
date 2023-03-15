
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "listy",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
        }

    def __help__(self, ctx):
        return """
            ls
            new <name>
                Creates a new list.
            delete <name>
                Deletes a list.

            add/remove <..options>
                Separate each item with a comma, first item is considered the list name to add to.
        """

    def __run__(self, ctx): 
        cmd, line = ctx.cmdsplit()
        #print(cmd, "-", line)
        data = ctx.get_data()
        match cmd:
            case "ls":
                for name, items in data.items():
                    ctx.writeln(f"{name}: ({len(items)}) {items}")
            case "new":
                data[line] = []
                ctx.save_data(data)
            case "delete":
                del data[line]
                ctx.save_data(data)
            case "add":
                ls = [item.strip() for item in line.split(",")]
                if len(ls) > 1:
                    name = ls[0]
                    ls.remove(name)
                    if data.get(name, None) != None:
                        for item in ls:
                            if item not in data[name]:
                                data[name].append(item)
                                ctx.writeln(f"Added '{item}'.")
                            else:
                                ctx.writeln(f"'{item}' was already in list.")
                        ctx.save_data(data)
                    else:
                        ctx.writeln("Invalid list.")

                else:
                    ctx.writeln("Not enough items.")
            case "remove":
                ls = [item.strip() for item in line.split(",")]
                if len(ls) > 1:
                    name = ls[0]
                    ls.remove(name)
                    if data.get(name, None) != None:
                        for item in ls:
                            if item in data[name]:
                                data[name].remove(item)
                                ctx.writeln(f"Removed '{item}'.")
                            else:
                                ctx.writeln(f"'{item}' wasn't in list.")
                        ctx.save_data(data)
                    else:
                        ctx.writeln("Invalid list.")

                else:
                    ctx.writeln("Not enough items.")

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

