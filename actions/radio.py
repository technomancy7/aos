import webbrowser
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "radio",
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
        if cmd == "": return ctx.writeln("Missing values.")
        match cmd:
            case "ls" | "list" | "lists":
                data = ctx.get_data_doc("radio")
                for cat in data.sections():
                    ctx.writeln(f" < {cat.string_key()} >")
                    for station in cat.sections():
                        d = station.field('description').optional_string_value() or ""
                        if d != "": d = d+"\n"
                        ctx.write_panel(f" < {station.string_key()} > \n{d}{station.field('url').optional_string_value()}\n{station.list('names').optional_string_values()}")

            case "show" | "get":
                pass

            case "open" | "web":
                data = ctx.get_data_doc("radio")
                for cat in data.sections():
                    for station in cat.sections():
                        n = station.string_key()
                        if ln.lower() == n.lower() or ln.lower() in station.list("names").optional_string_values():
                            if station.field('website').optional_string_value():
                                url = station.field('website').required_url_value()
                                webbrowser.open(url)
                            else:
                                ctx.writeln("Stream has no valid url.")

            case "play" | "p":
                data = ctx.get_data_doc("radio")

                for cat in data.sections():
                    for station in cat.sections():
                        n = station.string_key()
                        if ln.lower() == n.lower() or ln.lower() in station.list("names").optional_string_values():
                            if station.field('url').optional_string_value():
                                ctx.write_panel(f"Playing {station.field('url').optional_string_value()}")
                                ctx.play_audio_path(station.field('url').optional_string_value())
                                return
                            else:
                                ctx.writeln("Stream has no valid url.")
                ctx.writeln(f"Could not find station: {ln}")
            case "edit" | "e":
                ctx.edit_code("radio.eno")

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
