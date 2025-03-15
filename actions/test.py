
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "test",
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
            case "eno":
                doc = ctx.get_data(fmt="eno")
                print(doc)
            case "json":
                doc = ctx.get_data(fmt="json")
                print(doc)
                doc["test"] = "complete"
                doc["me"] = {"name": "Kaiser"}
                ctx.save_data(doc, fmt="json")
            case "toml":
                doc = ctx.get_data(fmt="toml")
                print(doc)
                doc["test"] = "complete"
                doc["me"] = {"name": "Kaiser"}
                ctx.save_data(doc, fmt="toml")
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
