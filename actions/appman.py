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

def on_help(ctx):
    return """ App Manager
    Commands:
        run <appname>
            Runs the command specified.

        show <appname>
            Show information on app.

        list
            Print list of known applications

        edit
            Open list in code editor

        dirs
            Show directory list

        launchers
            Show launcher list"""

def on_load(ctx):
    cmd = ctx.get_string_ind(0)
    line = ""
    if len(ctx.get_string_list()) > 1:
        line = ctx.get_string()[len(cmd)+1:]
    #data = ctx.get_data()
    data = ctx.get_data_doc("appman")
    #appdirs = data.get("appdirs", [])
    appdirs = data.section("Paths").list('Directories').optional_string_values() or []
    #extraapps = data.get("extraapps", [])
    extraapps = data.section("Paths").list('Apps').optional_string_values() or []

    min_match = ctx.touch_config("appman.min_match", 90)
    #appinfo = data.get("appinfo", {})
    appinfo = data.section("App Data")

    ignorepaths = data.section("Paths").list('Ignore Paths').optional_string_values() or []
    ignorenames = data.section("Paths").list('Ignore Names').optional_string_values() or []

    match cmd:
        case "run":
            def run_app(ctx, path, *args):
                ctx.writeln(f":right_arrow: {args} ")
                app = appinfo.section(path)
                #print(app)
                cwd = app.field("cwd").optional_string_value() or os.getcwd()
                #print("cwd: "+cwd)
                if path.endswith(".aos.py"):
                    with open(path) as f:
                        text = f.read()
                        to_compile = f'def func():\n{textwrap.indent(text, "  ")}'
                        env = {"ctx": ctx}
                        env.update(globals())
                        exec(to_compile, env)
                        env['func']()

                elif app.field("launcher").optional_string_value():
                    cmd = app.field("launcher").optional_string_value().replace("$F", path)
                    p = subprocess.run(cmd.split(), cwd=cwd)
                else:
                    def runit(rerun = False):
                        p = None
                        try:
                            p = subprocess.run([path, *args], cwd=cwd)
                        except PermissionError:
                            if rerun:
                                ctx.writeln("Could not update permissions automatically, launch failed.")
                                return

                            ctx.writeln(":right_arrow: Permissions error! Updating executable...")
                            os.system(f"chmod u+x {path}")
                            runit(rerun = True)

                        if ctx.touch_config("appman.show_result"):
                            ctx.writeln(f":right_arrow: Application exit: [blue]{p.args}[/blue] (Return code: "+str(p.returncode)+")")
                    runit()

            to_run = ctx.get_string_at(1)
            matches = []
            for d in appdirs:
                for filename in os.listdir(d):
                    if d+filename in ignorepaths: continue
                    if filename in ignorenames: continue

                    m = fuzz.ratio(line.lower(), filename.lower())
                    if min_match < m or filename.lower().startswith(to_run.lower()) or \
                    to_run.lower() in filename.lower():
                        matches.append(d+filename)

            for app in extraapps:
                if line.lower() == os.path.basename(app).lower():
                    matches.append(app)
                    break
                else:
                    m = fuzz.ratio(line.lower(), app.lower())
                    m2 = fuzz.ratio(line.lower(), os.path.basename(app).lower())
                    if min_match < m or os.path.basename(app).lower().startswith(to_run.lower()) or \
                    min_match < m2:
                        matches.append(app)

            args = ctx.lines[2:]

            if len(matches) == 0:
                ctx.say("No matches found.")

            elif len(matches) == 1:
                ctx.writeln(f":right_arrow: Launching {matches[0]}")
                run_app(ctx, matches[0], *args)

            else:
                ctx.say("Too many matches, select one: ")
                for i, m in enumerate(matches):
                    ctx.writeln(f"{i}. {m}")

                result = ctx.ask("index", prompt="Launch which app?")
                if result.isdigit():
                    result = int(result)
                    app = matches[result]
                    ctx.writeln(f":right_arrow: Launching {app}")
                    run_app(ctx, app, *args)

        case "show":
            if line == "":
                for v in appinfo.sections():
                    ctx.writeln(f"{v.string_key()}")
                    for el in v.fields():
                        ctx.writeln(f"[blue]{el.string_key()}[/blue] = {el.required_string_value()}")
                return

            for v in appinfo.sections():
                k = v.string_key()
                basename = os.path.basename(k)
                m = fuzz.ratio(line.lower(), basename.lower())
                if basename.lower() == line.lower() or basename.split(".")[0].lower() == line.lower() or \
                min_match < m:
                    ctx.writeln(f"[blue]Full Path[/blue] = [blue]{k}[/blue]")
                    for el in v.fields():
                        ctx.writeln(f"[blue]{el.string_key()}[/blue] = {el.required_string_value()}")

                    return
            ctx.writeln("No matching entries.")

        case "edit":
            ctx.edit_code(ctx.data_path()+"appman.eno")

        case "list":
            for d in appdirs:
                ctx.writeln(f"=== {d} ===")
                for filename in os.listdir(d):
                    if d+filename in ignorepaths: continue
                    if filename in ignorenames: continue
                    ctx.writeln("* "+filename)

                    p = appinfo.section(d+filename).field("description").optional_string_value()
                    if p:
                        ctx.writeln(f" - {p}")

            ctx.writeln("=== Others ===")
            for app in extraapps:
                ctx.writeln(app)

        case "dirs":
            for i, v in enumerate(appdirs):
                ctx.writeln(i, v)

        case "launchers":
            for i, v in enumerate(extraapps):
                ctx.writeln(i, v)


    return ctx
