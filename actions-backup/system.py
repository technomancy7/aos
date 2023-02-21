import os, importlib

def action_data():
    return {
    "name": "system",
    "author": "Kaiser",
    "version": "0.2",
    "features": [],
    "group": "system",
}

def on_help(ctx):
    return """
    System commands
    Generic utilities for AOS

    Commands:
        purgelog
            - Clears the log file.
        actions
            - Lists available installed actions
    """
def on_load(ctx): 
    if ctx.get_string_ind(0) == "purgelog":
        with open(ctx.aos_dir+"self.log", "w+") as f:
            f.write("")

    elif ctx.get_string_ind(0) == "actions":
        directory = ctx.aos_dir+"actions/"
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f) and filename != "system.py":
                f = importlib.import_module("actions."+filename.split(".")[0])
                if hasattr(f, "action_data"):
                    d = f.action_data()
                    ctx.writeln(f"[yellow]{d.get('name', filename)}[/yellow] (v {d.get('version', '0')}) by {d.get('author', '?')}")
                else:
                    ctx.writeln(f"{filename.split('.')[0]} has no action_data property.", style="dim")
    return ctx

