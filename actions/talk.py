import os
from tools.datascript import *
from tools.dataspeak import *

def action_data():
    return {
    "name": "talk",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

speaker = Dataspeak()

def on_help(ctx):
    pass

def hook(ctx, line):
    if not line.startswith("."): return False
    cmd = line.split(" ")[0][1:]
    arg = " ".join(line.split(" ")[1:])

    match cmd:
        case "load":
            parser = Datascript()
            if ctx.has_flag("o"): 
                print("Purging history...")
                speaker.tree = []
                
            print("Loading from file: ",arg)
            print("")
            parser.parse_file(arg)
            vars = parser.variables
            for key, block in vars.items():
                if type(block) != dict: continue
                speaker.load(block)

            #print(speaker.tree)
            print("Export to",ctx.data_path())
            data = speaker.export()
            #print(data)
            ctx.save_data(data)

def on_load(ctx): 
    data = ctx.get_data()
    speaker.variables = data.get("variables", {})
    speaker.tree = data.get("tree", [])

    line = ctx.get_string()

    if line == "":
        while True:
            line = input("> ")
            if not hook(ctx, line):
                response = speaker.read(line)
                print(response)
    else:
        if not hook(ctx, line):
            response = speaker.read(line)
            print(response)

    return ctx

