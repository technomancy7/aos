
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "$DEFAULT_NAME",
            "author": "$DEFAULT_AUTHOR",
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
        # Main functionality here.
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
