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

def customize(ctx, dsc):
    def raos(engine, line):
        engine.echo("Successful connection to customize.")
        engine.echo(f"Got line {line}")
    dsc.commands["aos"] = raos
    return dsc

def on_load(ctx): 
    cmd = ctx.get_string_ind(0)
    show_data = not ctx.has_flag("silent")

    if cmd == "run":
        file = ctx.get_string()[len(cmd)+1:]
        if not file.endswith(".dsc"):
            file = file+".dsc"

        if "/" not in file:
            file = ctx.aos_dir+"dsc/"+file
        print(file)
        parser = Datascript()
        customize(ctx, parser)
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
