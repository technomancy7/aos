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
                data = ctx.get_data("radio", fmt="toml")
                for radio_key, station in data.items():
                    text = f" < [blue]{station.get('title') or radio_key}[/blue] >"
                    text += f"\n[red]Stream[/red]: {station.get('url', '')}"
                    text += f"\n[red]Web[/red]: {station.get('website', '')}"
                    text += f"\n[red]Names[/red]: {station.get('names', [])}"
                    ctx.write_panel(text)

            case "open" | "web":
                data = ctx.get_data("radio", fmt="toml")
                for radio_key, station in data.items():
                    if radio_key == ln or ln in station.get("names", []):
                        ctx.writeln(f"Opening {station['website']}")
                        webbrowser.open(station['website'])

            case "play" | "p":
                data = ctx.get_data("radio", fmt="toml")
                for radio_key, station in data.items():
                    if radio_key == ln or ln in station.get("names", []):
                        if station.get("url"):
                            ctx.write_panel(f"Playing {station['url']}")
                            ctx.play_audio_path(station['url'])
                            return
                        else:
                            ctx.writeln("Stream has no valid url.")
                ctx.writeln(f"Could not find station: {ln}")

            case "edit" | "e":
                ctx.edit_code("radio.toml")

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
