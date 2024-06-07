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
    """
def on_load(ctx):
    if ctx.get_string_ind(0) == "purgelog":
        with open(ctx.aos_dir+"self.log", "w+") as f:
            f.write("")
            
    return ctx
