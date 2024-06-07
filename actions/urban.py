import requests, textwrap
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "urban",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __call_api__(self, term):
        url = f"https://api.urbandictionary.com/v0/define?term={term.replace(' ', '+')}"
        return requests.get(url).json()['list']

    def __help__(self, ctx):
        return """
            Default help.
        """

    def __run__(self, ctx):
        term = ctx.get_string()
        data = self.__call_api__(term)
        for entry in data:
            text = f"({entry['word']})\n{entry['definition']}\n\nExample: \n{textwrap.indent(entry['example'], '    ')}\n\n - By {entry['author']} on {entry['written_on']}. (+ {entry['thumbs_up']} / - {entry['thumbs_down']})"
            ctx.write_panel(ctx.esc(text))
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
