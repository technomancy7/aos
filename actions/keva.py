
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
            rm <key>
            ls
        """

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()

        match cmd:
            case "set":
                k = ln.split()[0]
                v = ' '.join(ln.split()[1:])
                g = ""
                if "." in k:
                    g = k.split(".")[0]
                    k = k.split(".")[1]

                if g:
                    data = ctx.get_data()

                    if data.get(g, None) == None and type(data.get(g)) != dict:
                        ctx.writeln(f"Created key group: {g}")
                        data[g] = {}

                    if type(data.get(g)) != dict:
                        return ctx.writeln("Key is already taken.")

                    data[g][k] = v
                    ctx.save_data(data)
                    ctx.writeln(f"{g}.{k} = {v}")
                else:
                    data = ctx.get_data()
                    data[k] = v
                    ctx.save_data(data)
                    ctx.writeln(f"{k} = {v}")

            case "get":
                data = ctx.get_data()

                if "." in ln:
                    g = ln.split(".")[0]
                    k = ln.split(".")[1]
                    group = data.get(g)
                    if type(group) != dict:
                        return ctx.writeln(f"{g} not a valid group.")
                    if group != None:
                        v = group.get(k)
                        if v != None:
                            ctx.writeln(f"{g}.{k} = {v}")
                        else:
                            ctx.writeln(f"{g}.{k} (Undefined)")
                    else:
                        ctx.writeln(f"{g} (Undefined)")
                else:
                    v = data.get(ln)
                    if v != None:
                        ctx.writeln(f"{ln} = {v}")
                    else:
                        ctx.writeln(f"{ln} (Undefined)")

            case "rm":
                data = ctx.get_data()

                if "." in ln:
                    g = ln.split(".")[0]
                    k = ln.split(".")[1]
                    group = data.get(g)
                    if type(group) != dict:
                        return ctx.writeln(f"{g} not a valid group.")
                    if group != None:
                        v = group.get(k)
                        if v != None:
                            del data[g][k]
                            ctx.writeln(f"{g}.{k} (Deleted) {v}")
                            ctx.save_data(data)
                        else:
                            ctx.writeln(f"{g}.{k} (Undefined)")
                    else:
                        ctx.writeln(f"{g} (Undefined)")
                else:
                    v = data.get(ln)
                    if v != None:
                        del data[ln]
                        ctx.writeln(f"{ln} (Deleted) {v}")
                        ctx.save_data(data)
                    else:
                        ctx.writeln(f"{ln} (Undefined)")

            case "ls":
                data = ctx.get_data()
                for k, v in data.items():
                    if type(v) == dict:
                        ctx.writeln(f" [ {k} ]")
                        for sk, sv in v.items():
                            ctx.writeln(f" | {sk} = {sv}")
                    else:
                        ctx.writeln(f"{k} = {v}")

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
