import requests # import requests for the api call
from tools.you import You

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "you",
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
        yc = You(ctx.touch_config("keys.youdotcom"))
        #yc.chatmodel = yc.MODEL_BETTERCHAT
        match cmd:
            case "chat":
                r = yc.chat(ln)
                ctx.say(r)
            case "imagine":
                r = yc.imagine(ln)
                ctx.say(r)
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

