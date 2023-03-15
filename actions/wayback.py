import requests, webbrowser

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "wayback",
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
        url = f"https://archive.org/wayback/available?url={ln}"
        test = 1
        js = requests.get(url).json()
        print(js)
        if js['archived_snapshots']:
            if ctx.has_flag("open"):
                webbrowser.open(js['archived_snapshots']['closest']['url'])
            else:
                ctx.say("Found a result. Pass the --open flag to automatically open the site in your browser.")
                ctx.writeln(f"URL: {js['archived_snapshots']['closest']['url']}")

        else:
            ctx.say("No results.")
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

