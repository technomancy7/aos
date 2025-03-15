import os, mimetypes

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "cb",
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

    def set_clip(self, value, *, cut = False, cb = "default"):
        clip = {
            "value": value,
            "mimetype": "",
            "cut": cut
        }
        if os.path.exists(value):
            clip['mimetype'] = mimetypes.guess_type(value)[0]
        else:
            clip['mimetype'] = "aos/plaintext"

        d = self.ctx.get_data(override = "cb") # just to ensure this stays as cb context even if called by other commands
        d[cb] = clip
        self.ctx.save_data(d, override = "cb")



    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()
        # Main functionality here.

        match cmd:
            case "cp" | "copy":
                self.set_clip(ln, cb = ctx.get_flag("b", "default"))

            case "ls":
                d = ctx.get_data()
                print(d)

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
