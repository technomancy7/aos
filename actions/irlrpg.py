
class Action:
    def action_data(self):
        return {
            "name": "irlrpg",
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
        # Main functionality here.
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

