from pypresence import Presence
import time
import sys, os, subprocess
#TODO support for dynamic applications, reading when something is running
# implement similar to custom message mode, but instead it scans for processes based on patterns in eno script
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "discord",
            "author": "Techno",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            Flags:
                delay d:(1200)
                player p:(firefox)
                displayplayer dp:
                icon i:(kde,chromium,firefox,vivaldi,youtube)
                fmt f:{{artist}} - {{title}}
                client: 0
                custom_msg msg:
                custom_state state:
        """

    def __run__(self, ctx):
        ln = ctx.get_string()

        custom_msg = ""
        if ctx.has_flag("msg"):
            custom_msg = ctx.get_flag("msg")

        custom_state = ""
        if ctx.has_flag("state"):
            custom_state = ctx.get_flag("state")

        delay = ctx.touch_config("discord.delay", 1200)
        if ctx.has_flag("d"):
            delay = int(ctx.get_flag("d"))

        if custom_msg != "":
            delay = delay * 1000
        player = ctx.touch_config("discord.player", "firefox")
        if ctx.has_flag("p"):
            player = ctx.get_flag("p")

        displayplayer = ctx.touch_config("discord.displayplayer", "")
        if ctx.has_flag("dp"):
            displayplayer = ctx.get_flag("dp")

        if displayplayer == "":
            displayplayer = player

        icon = ctx.touch_config("discord.icon", "kde")
        if ctx.has_flag("i"):
            icon = ctx.get_flag("i")


        fmt = ctx.touch_config("discord.fmt", "{{artist}} - {{title}}")
        if ctx.has_flag("f"):
            fmt = ctx.get_flag("f")

        client_id = ctx.touch_config("discord.client_id", 0)  # Fake ID, put your real one here
        if ctx.has_flag("client"):
            client_id = ctx.get_flag("client")

        print(f"Connecting to discord via {client_id} / DELAY {delay} / PLAYER {player} ({displayplayer}) / ICON {icon} / FMT {fmt}")

        RPC = Presence(client_id)  # Initialize the client class
        RPC.connect() # Start the handshake loop
        ctx.notify("Status update", f"Connected to Discord RPC.")
        last_details = ""


        while True:  # The presence will stay on as long as the program is running
            details = ""
            if custom_msg == "":
                try:
                    output = subprocess.check_output(["playerctl", "metadata", "--format", fmt, "-p", player])
                    details = output.decode("utf-8").strip()
                except subprocess.CalledProcessError:
                    details = "No media playing"

                if details != last_details:
                    d = RPC.update(state=f"Playing in {displayplayer}", details=f"{details}", large_image="infinity-transparent", large_text="Designed by @_technomancer",  small_image=icon, small_text=displayplayer, start=time.time(), buttons=[{"label": "Source", "url": "https://github.com/technomancy7/synthlink"}, {"label": "Deus Ex Community", "url": "https://discord.gg/deus-ex-community-hq-396716931962503169"}])
                    update = d['data']
                    print(f"state update @ {update['name']}: {update['state']} / {update['details']}")
                    last_details = details
                    ctx.notify("Status update", f"{update['name']}: {update['state']} / {update['details']}")
            else:
                d = RPC.update(state=custom_state or f"Message from Techno.", details=f"{custom_msg}", large_image="infinity-transparent", large_text="Designed by @_technomancer",  small_image="kde", small_text="Custom Message", start=time.time(), buttons=[{"label": "Source", "url": "https://github.com/technomancy7/synthlink"}, {"label": "Deus Ex Community", "url": "https://discord.gg/deus-ex-community-hq-396716931962503169"}])
                update = d['data']
                print(f"state update @ {update['name']}: {update['state']} / {update['details']}")
                last_details = details
            time.sleep(delay)

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
