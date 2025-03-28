from tools.converters import XConverter

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "convert",
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
        line = ctx.get_string().split(" ")
        c = XConverter()
        if line[2] == "miles":
            line[2] = "mile"
        r = c.pretty_convert(line[0], line[1], line[2])
        ctx.say(r)

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
