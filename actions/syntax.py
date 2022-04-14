import os, importlib

def action_data():
    return {
    "name": "syntax",
    "author": "Kaiser",
    "version": "0",
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
    from rich.console import Console
    from rich.syntax import Syntax
    from rich.markdown import Markdown

    console = Console()
    

    if path.endswith("md") or ctx.has_flag("md"):
        with open(path) as f:
            md = Markdown(f.read())
            console.print(md)
    else:
        syntax = Syntax.from_path(path)
        console.print(syntax)

    return ctx
