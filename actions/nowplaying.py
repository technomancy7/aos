from pypresence import Presence
import time
import sys, os, subprocess
        
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "youtubemusic",
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

    def __gui__(self, sender, app, data):
        label = data['label']
        context = data['context']
        pos = context.touch_config(f"gui.{label}_pos", [0, 19])
        height = context.touch_config(f"gui.{label}_height", 0)
        width = context.touch_config(f"gui.{label}_width", 0)

        if data["init"](label):
            dpg = data['dpg']
            with dpg.window(label=label, tag=label, pos = pos, width = width, height = height, on_close = lambda: data["close"](label)):
                dpg.add_button(callback=None, label=label)

    def __run__(self, ctx): 
        ln = ctx.get_string()
        
        delay = ctx.touch_config("nowplaying.delay", 1200)
        if ctx.has_flag("d"):
            delay = int(ctx.get_flag("d"))
            
        player = ctx.touch_config("nowplaying.player", "firefox")
        if ctx.has_flag("p"):
            player = ctx.get_flag("p")

        displayplayer = ctx.touch_config("nowplaying.displayplayer", "")
        if ctx.has_flag("dp"):
            displayplayer = ctx.get_flag("dp")

        if displayplayer == "":
            displayplayer = player

        icon = ctx.touch_config("nowplaying.icon", "kde")
        if ctx.has_flag("i"):
            icon = ctx.get_flag("i")


        fmt = ctx.touch_config("nowplaying.fmt", "{{artist}} - {{title}}")
        if ctx.has_flag("f"):
            fmt = ctx.get_flag("f")
            
        client_id = ctx.touch_config("nowplaying.client_id", 0)  # Fake ID, put your real one here
        
        print(f"Connecting to discord via {client_id} / DELAY {delay} / PLAYER {player} ({displayplayer}) / ICON {icon} / FMT {fmt}")
        RPC = Presence(client_id)  # Initialize the client class
        RPC.connect() # Start the handshake loop
        
        last_details = ""


        while True:  # The presence will stay on as long as the program is running
            details = ""
            
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
                
            time.sleep(delay)

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

