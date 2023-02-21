import sys, importlib, inspect

def action_data():
    return {
    "name": "scriptkiddie",
    "author": "Kai",
    "version": "0.0",
    "features": [],
    "group": "",
}

def on_help(ctx):
    return """

    """


def on_load(ctx): 
    data_dir = ctx.data_path()
    sys.path.append(data_dir)
    f = importlib.import_module("corekiddie")
    print(f)
    kid = f.Corekid(ctx)
    kid.load("Kara")
    print(kid.dump())
    return ctx

