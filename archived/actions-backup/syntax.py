import os, importlib

def action_data():
    return {
    "name": "syntax",
    "author": "Kaiser",
    "version": "0.1a",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return """
    Uses the Rich library to print a code file.

    Takes one parameter: path to file
    """

def on_load(ctx): 
    path = ctx.get_string()
    from rich.syntax import Syntax
    from rich.markdown import Markdown

    

    if path.endswith("md") or ctx.has_flag("md"):
        with open(path) as f:
            md = Markdown(f.read())
            ctx.writeln(md)
    else:
        syntax = Syntax.from_path(path)
        ctx.writeln(syntax)

    return ctx

