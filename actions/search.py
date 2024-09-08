import textwrap
import webbrowser
import urllib.parse


class Action:
    @staticmethod
    def __action__():
        return {
            "name": "search",
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
        ln = ctx.get_string()

        if ctx.has_flag("reset"):
            ctx.writeln("Creating default templates...")
            engines = textwrap.dedent("""\
            brave: https://search.brave.com/search?q=%s&source=web
            amazon: https://www.amazon.co.uk/s?k=%s
            presearch: https://presearch.com/search?q=%s
            startpage: https://www.startpage.com/do/search?sc=iVMkG7zldRGW20&query=%s&cat=web&qloc=eyJ0eXBlIjogIm5vbmUifQ%3D%3D
            duckduckgo: https://duckduckgo.com/?t=h_&q=%s&ia=web
            ddg: https://duckduckgo.com/?t=h_&q=%s&ia=web
            youtube: https://www.youtube.com/results?search_query=%s
            yt: https://www.youtube.com/results?search_query=%s
            """)
            ctx.save_data_file(engines, "data.eno")

        elif ctx.has_flag("ls"):
            engines = ctx.get_data_doc()
            for f in engines.fields():
                ctx.writeln(f"[blue]{f.string_key()}[/blue]: {f.required_string_value()}")
        else:
            witheng = ctx.touch_config("search.engine", "brave")
            if ctx.has_flag("e"):
                witheng = ctx.get_flag("e")
            engines = ctx.get_data_doc()
            url = engines.field(witheng).required_string_value().replace("%s", urllib.parse.quote(ln))

            if ctx.has_flag("b"):
                webbrowser.get(ctx.get_flag("b")).open(url)
            else:
                webbrowser.open(url)

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
