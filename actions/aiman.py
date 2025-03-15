import os, json, subprocess, shutil, sys, textwrap, re, requests
from thefuzz import fuzz, process
import shlex, importlib
import importlib.util as ilu
from urllib.parse import urlparse

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "aiman",
            "author": "Kaiser",
            "version": "0.0",
            "features": [],
            "group": "system",
    }

    def __help__(self, ctx):
        return """ AppImage Manager
        Commands:
            run <appname>
                Runs the command specified.

            list
                Print list of known applications
        """

    def __run__(self, ctx):
        cmd, line = ctx.cmdsplit()

        data = ctx.get_data("appman", fmt="toml")
        min_match = ctx.touch_config("aiman.min_match", 90)
        aimpath = ctx.touch_config("aiman.appimages", "")
        if not aimpath:
            return ctx.write(f"Config `aiman.appimages` needs to be defined to the path where your appimages are stored.")
        
        match cmd:
            case "run":
                def run_app(launcher, *args):
                    p = None
                    print("Running", launcher, list(args))
                    try:
                        p = subprocess.run([aimpath+launcher, *args])
                    except PermissionError:
                        ctx.writeln(":right_arrow: Permissions error! Updating executable...")
                        os.system(f"chmod u+x {aimpath+launcher}")
                        ctx.writeln(":right_arrow: chmod'd the executable, try running again.")
                                
                    if p != None:
                        if ctx.touch_config("appman.show_result"):
                            ctx.writeln(f":right_arrow: Application exit: [blue]{p.args}[/blue] (Return code: "+str(p.returncode)+")")
                    
                to_run = line.split(" ")[0]
                matches = []

                for filename in os.listdir(aimpath):
                    fmt = filename.split(".")[0]
                    m = fuzz.ratio(line.lower(), fmt.lower())

                    if min_match < m or fmt.lower().startswith(to_run.lower()) or \
                    to_run.lower() in fmt.lower():
                        matches.append(filename)

                args = ctx.lines[2:]

                if len(matches) == 0:
                    ctx.say("No matches found.")

                elif len(matches) == 1:
                    ctx.writeln(f":right_arrow: Launching {matches[0]}")
                    run_app(matches[0], *args)

                else:
                    ctx.say("Too many matches, select one: ")
                    for i, m in enumerate(matches):
                        ctx.writeln(f"{i}. {m}")

                    result = ctx.ask("index", prompt="Launch which app?")
                    if result.isdigit():
                        result = int(result)
                        app = matches[result]
                        ctx.writeln(f":right_arrow: Launching {app}")
                        run_app(app, *args)

            case "get":
                pass

            case "list" | "ls":
                for filename in os.listdir(aimpath):
                    ctx.writeln("* "+filename)


        return ctx
