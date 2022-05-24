from tools.datascript import *
import os

def action_data():
    return {
    "name": "datascript",
    "author": "Kaiser",
    "version": "0.9",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    pass

def on_load(ctx): 
    cmd = ctx.get_string_ind(0)
    show_data = ctx.has_flag("show")

    if cmd == "run":
        file = ctx.get_string()[len(cmd)+1:]
        if not file.endswith(".dsc"):
            file = file+".dsc"
        parser = Datascript()
        parser.writeln = ctx.writeln
        dc = parser.parse_file(file)
        if show_data: print(dc)

    else:
        parser = Datascript()
        parser.writeln = ctx.writeln
        while True:
            l = input(parser.getv('_current_block')+"> ")
            parser.readline(l)

    return ctx
