import os

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "search",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
        }

    def __help__(self, ctx):
        return """
            Default help.
        """

    def __run__(self, ctx): 
        ln = ctx.get_string()
        search_directories = [
            os.path.expanduser("~/")
        ]

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

