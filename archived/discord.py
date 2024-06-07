from pypresence import Presence
import time
import sys, os

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "discord",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            Default help.

            discord <string to display>

            --nr : disable refresh regardless of config (discord.refresh)
            --r : enable refresh regardless of config (discord.refresh)
            --delay:<int> : set delay time regardless of config (discord.delay)
        """

    def __run__(self, ctx):
        ln = ctx.get_string()
        delay = ctx.touch_config("discord.delay", 1200)
        if ctx.has_flag("d"):
            delay = int(ctx.get_flag("d"))
        do_refresh = ctx.touch_config("discord.refresh", True)
        if ctx.has_flag("r"): do_refresh = True
        if ctx.has_flag("nr"): do_refresh = False
        client_id = ctx.touch_config("discord.client_id", 1128669396844412939)  # Fake ID, put your real one here

        print(f"Connecting to discord via {client_id} / REFRESH {do_refresh} / DELAY {delay}")
        RPC = Presence(client_id)  # Initialize the client class
        RPC.connect() # Start the handshake loop

        def update():
            state = None
            if os.path.exists(f"{ctx.aos_dir}discord.txt"):
                with open(f"{ctx.aos_dir}discord.txt") as f:
                    state = f.read()
            print("state update: ", RPC.update(state=state, details=ln, large_image="athena", small_image="athena"))

        if not do_refresh:
            update()
        #line1 = "Techno's WIP Kate extension"
        #line2 = "Working on stuff."
        while True:  # The presence will stay on as long as the program is running
            if do_refresh:
                update()
            #print("arg", sys.argv)
            time.sleep(delay) # Can only update rich presence every 15 seconds

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
