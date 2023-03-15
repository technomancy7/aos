import os, json, subprocess, shutil, sys, textwrap
from thefuzz import fuzz, process
import shlex, importlib
import importlib.util as ilu
def action_data():
    return {
        "name": "appman",
        "author": "Kaiser",
        "version": "0.0",
        "features": [],
        "group": "system",
}
open_file_name = ""

def on_help(ctx):
    return """   

    Commands:
        run <appname>
            Runs the command specified.

        show <appname>

        list

        add_directory <dir>

        add_launcher <dir>
    """

def on_load(ctx): 
    cmd = ctx.get_string_ind(0)
    line = ""
    if len(ctx.get_string_list()) > 1:
        line = ctx.get_string()[len(cmd)+1:]
    data = ctx.get_data()
    appdirs = data.get("appdirs", [])
    extraapps = data.get("extraapps", [])
    min_match = ctx.touch_config("appman.min_match", 90)
    appinfo = data.get("appinfo", {})

    def get_prop(ctx, app, key, de = None):
        if appinfo.get(app, {}):
            if appinfo[app].get(key, de) != de:
                return appinfo[app][key]

        return de

    match cmd:
        
        case "run":
            def run_app(ctx, path, *args):
                print(args)
                
                print("Run", path, "with", *args)
                app = appinfo.get(path, {})
                print(app)
                cwd = app.get("cwd", None) or os.getcwd()
                if path.endswith(".aos.py"):
                    with open(path) as f:
                        text = f.read()
                        to_compile = f'def func():\n{textwrap.indent(text, "  ")}'
                        env = {"ctx": ctx}
                        env.update(globals())
                        exec(to_compile, env)
                        env['func']()

                elif app.get("launcher", "") != "": #@todo finish and test this
                    return print("Not supported yet.")
                    cmd = app['launcher']
                    p = subprocess.run([cmd, *args], cwd=cwd)
                else:
                    def runit():
                        p = None
                        try:
                            p = subprocess.run([path, *args], cwd=cwd)
                        except PermissionError:
                            ctx.writeln("Permissions error! Updating executable...")
                            os.system(f"chmod u+x {path}")
                            runit()
                        
                        if ctx.touch_config("appman.show_result"): 
                            ctx.writeln(f"Application exit: [blue]{p.args}[/blue] (Return code: "+str(p.returncode)+")")
                    runit()
                    
            to_run = ctx.get_string_at(1)
            matches = []
            for d in appdirs:
                for filename in os.listdir(d):
                    m = fuzz.ratio(line.lower(), filename.lower())
                    if min_match < m or filename.lower().startswith(to_run.lower()) or to_run.lower() in filename.lower():
                        matches.append(d+filename)

            for app in extraapps:
                m = fuzz.ratio(line.lower(), app.lower())
                if min_match < m or app.lower().startswith(to_run.lower()) or to_run.lower() in app.lower():
                    matches.append(app)

            args = ctx.lines[2:]
            
            if len(matches) == 0:
                ctx.say("No matches found.")
            elif len(matches) == 1:
                ctx.writeln(f"Launching {matches[0]}")
                run_app(ctx, matches[0], *args)
            else:
                ctx.say("Too many matches, select one: ")
                for i, m in enumerate(matches):
                    ctx.writeln(f"{i}. {m}")
                
                result = ctx.ask("Launch which app?")
                if result.isdigit():
                    result = int(result)
                    app = matches[result]
                    ctx.writeln(f"Launching {app}")
                    run_app(ctx, app, *args)
        
        case "set":
            if "/" not in line:
                line = os.getcwd()+"/"+line
            else:
                os.path.expanduser(line)

            ctx.writeln(f"Setting config for {line}")
            key = ctx.ask("Key")
            value = ctx.ask("Value")
            ctx.writeln(key, value)
            a = appinfo.get(line, {})
            a[key] = value
            appinfo[line] = a
            data["appinfo"] = appinfo
            ctx.save_data(data)

        case "list":
            for d in appdirs:
                ctx.writeln(f"=== {d} ===")
                for filename in os.listdir(d):
                    ctx.writeln("* "+filename)
                    p = get_prop(ctx, d+filename, "description", "")

                    if p != "":
                        ctx.writeln(f" - {p}")

            ctx.writeln("=== Others ===")
            for app in extraapps:
                ctx.writeln(app)

        case "add_directory":
            if line == "." or line == "":
                line = os.getcwd()+"/"
            else:
                os.path.expanduser(line)
            if not line.endswith("/"):
                line = line+"/"
            if line in appdirs:    
                return ctx.say("Directory already added.")
            ctx.writeln(f"Added > {line}")
            appdirs.append(line)
            data["appdirs"] = appdirs
            print(data)
            ctx.save_data(data)
            ctx.say("Directory added.")

        case "add_launcher":
            if "/" not in line:
                line = os.getcwd()+"/"+line
            else:
                os.path.expanduser(line)

            if line in extraapps:    
                return ctx.say("Launcher already added.")

            ctx.writeln(f"Added > {line}")
            extraapps.append(line)
            data["extraapps"] = extraapps
            print(data)
            ctx.save_data(data)
            ctx.say("Launcher added.")

    return ctx
