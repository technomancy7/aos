
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "actstore",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            Default help.
        """

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()
        # Main functionality here.
        match cmd:
            case "set" | "s":
                d = ctx.get_data()
                db = ctx.get_flag("n", "default")
                d[db] = ln
                ctx.save_data(d)
                ctx.writeln(f"Saved {ln} -> {db}")
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
