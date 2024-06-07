import requests
from urllib.parse import quote
from textwrap import dedent
import webbrowser

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "wiki",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """\
        Shows summary of search term.

        Flags:
            --browser : opens in web browser
            --simple : only shows result
        """

    def __run__(self, ctx):
        ln = ctx.get_string()
        simple_mode = ctx.has_flag("simple")
        open_in_browser = ctx.has_flag("browser")

        if open_in_browser:
            ln = quote(ln)
            base = "https://en.wikipedia.org/"
            if not simple_mode: ctx.writeln(f":right_arrow: Finding relevant pages...")
            r = requests.get(f"{base}w/api.php?action=opensearch&search={ln}&limit=1&format=json").json()

            if len(r[3]) > 0:
                addr = r[3][0]
                name = webbrowser.get().name
                if not simple_mode: ctx.writeln(f":right_arrow: Opening in browser {name}: {addr}")
                webbrowser.open(addr)
            else:
                ctx.writeln("No results.")
            return

        if ln:
            if not simple_mode: ctx.writeln(f":right_arrow: Searching for: {ln}...")
            ln = quote(ln)
            base = "https://en.wikipedia.org/"
            r = requests.get(f"{base}w/api.php?action=opensearch&search={ln}&limit=1&format=json").json()

            if len(r[3]) > 0:
                addr = r[3][0]
                if not simple_mode: ctx.writeln(f":right_arrow: Got base address: {addr}")
                apiaddr = addr.replace("/wiki/", "/api/rest_v1/page/summary/")
                if not simple_mode: ctx.writeln(f":right_arrow: Converted to API address: {apiaddr}")

                fresult = requests.get(apiaddr).json()

                if not simple_mode: ctx.write_panel(f""" < {fresult['title']} ({fresult['description']}) >\n[blue]{fresult['extract']}""")

                if simple_mode: ctx.writeln(fresult['extract'])
            else:
                ctx.writeln("No results.")
        else:
            ctx.writeln("Summarize what?")
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
