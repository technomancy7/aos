
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "keva",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            set <key> <value>
            get <key>
            rm | remove | rem | delete | del <key>
            ls | list
        """

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()

        match cmd:
            case "set":
                if ln == "":
                    k = ctx.g.ask("Key: ")
                    v = ctx.g.ask("Value:")
                else:
                    k = ln.split()[0]
                    v = ' '.join(ln.split()[1:])

                g = ""
                if "." in k:
                    g = k.split(".")[0]
                    k = k.split(".")[1]

                if g:
                    data = ctx.get_data()

                    if data.get(g, None) == None and type(data.get(g)) != dict:
                        ctx.writeln(f"Created key group: [blue]{g}[/blue]")
                        data[g] = {}

                    if type(data.get(g)) != dict:
                        return ctx.writeln(f"Key [blue]{g}[/blue] is already taken.")

                    data[g][k] = v
                    ctx.save_data(data)
                    ctx.writeln(f"[blue]{g}[/blue].[blue]{k}[/blue] = [yellow]{v}[/yellow]")
                else:
                    data = ctx.get_data()
                    data[k] = v
                    ctx.save_data(data)
                    ctx.writeln(f"[blue]{k}[/blue] = [yellow]{v}[/yellow]")

            case "get":
                data = ctx.get_data()

                if "." in ln:
                    g = ln.split(".")[0]
                    k = ln.split(".")[1]
                    group = data.get(g)
                    if type(group) != dict:
                        return ctx.writeln(f"[blue]{g}[/blue] not a valid group.")
                    if group != None:
                        v = group.get(k)
                        if v != None:
                            ctx.writeln(f"[blue]{g}[/blue].[blue]{k} = [green]{v}[/green]")
                        else:
                            ctx.writeln(f"[blue]{g}[/blue].[blue]{k} ([yellow]Undefined[/yellow])")
                    else:
                        ctx.writeln(f"[blue]{g}[/blue] ([yellow]Undefined[/yellow])")
                else:
                    v = data.get(ln)
                    if v != None:
                        ctx.writeln(f"[blue]{ln}[/blue] = [green]{v}[/green]")
                    else:
                        ctx.writeln(f"[blue]{ln}[/blue] ([yellow]Undefined[/yellow])")

            case "rm" | "rem" | "remove" | "del" | "delete":
                data = ctx.get_data()

                if "." in ln:
                    g = ln.split(".")[0]
                    k = ln.split(".")[1]
                    group = data.get(g)
                    if type(group) != dict:
                        return ctx.writeln(f"[blue]{g}[/blue] not a valid group.")
                    if group != None:
                        v = group.get(k)
                        if v != None:
                            del data[g][k]
                            ctx.writeln(f"[blue]{g}[/blue].[blue]{k}[/blue] ([red]Deleted[/red]) {v}")
                            ctx.save_data(data)
                        else:
                            ctx.writeln(f"[blue]{g}[/blue].[blue]{k}[/blue] ([yellow]Undefined[/yellow])")
                    else:
                        ctx.writeln(f"[blue]{g}[/blue] ([yellow]Undefined[/yellow])")
                else:
                    v = data.get(ln)
                    if v != None:
                        del data[ln]
                        ctx.writeln(f"[blue]{ln}[/blue] ([red]Deleted[/red]) {v}")
                        ctx.save_data(data)
                    else:
                        ctx.writeln(f"[blue]{ln}[/blue] ([yellow]Undefined[/yellow])")

            case "ls" | "list":
                data = ctx.get_data()
                for k, v in data.items():
                    if type(v) == dict:
                        ctx.writeln(f" [ [blue]{k}[/blue] ]")
                        for sk, sv in v.items():
                            ctx.writeln(f" | [blue]{sk}[/blue] = {sv}")
                    else:
                        ctx.writeln(f"[blue]{k}[/blue] = {v}")

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
