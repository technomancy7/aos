import os
from tools.datascript import *
from tools.dataspeak import *

def action_data():
    return {
    "name": "talk",
    "author": "Kaiser",
    "version": "0.4",
    "features": [],
    "group": "system",
}

speaker = Dataspeak()

def on_help(ctx):
    pass

def hook(ctx, line):
    if not line.startswith("."): return False
    cmd = line.split(" ")[0][1:]
    arg = " ".join(line.split(" ")[1:])

    match cmd:
        case "loaddir":
            parser = Datascript()
            if ctx.has_flag("o"): 
                print("Purging history...")
                speaker.tree = []
                
            if arg == "": arg = ctx.aos_dir+"dsc/speech/"
            print("Loading from dir: ",arg)
            print("")
            parser.parse_dir(arg)
            vars = parser.variables
            for key, block in vars.items():
                if type(block) != dict: continue
                speaker.load(block)

            #print(speaker.tree)
            print("Export to",ctx.data_path())
            data = speaker.export()
            #print(data)
            ctx.save_data(data)

        case "load":
            parser = Datascript()
            if ctx.has_flag("o"): 
                print("Purging history...")
                speaker.tree = []

            if arg == "": arg = ctx.aos_dir+"dsc/speech/main.dsc"
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
    ctx.set_config("talk.active", True)
    data = ctx.get_data()
    speaker.variables = data.get("variables", {})
    speaker.tree = data.get("tree", [])
    speaker.default_response = data.get("default_response", [])
    line = ctx.get_string()
    username = ctx.username()


    if line == "":
        while True:
            line = input(f"({username})> ")
            if not hook(ctx, line):
                response = speaker.read(line)
                if response == None:
                    print("No response.")
                    continue
                #print(response["text"])
                ctx.say(response["text"])
                cmd = response["command"]
                if cmd != "":
                    ctx.update_from_line(cmd)
                    ctx.execute()
                    if ctx.response["data"].get("tts"):
                        ctx.say(ctx.response["data"]["tts"])
    else:
        if not hook(ctx, line):
            response = speaker.read(line)
            if response == None:
                print("No response.")
                return
            ctx.say(response["text"])
            #print(response["text"])
            cmd = response["command"]
            if cmd != "":
                ctx.update_from_line(cmd)
                ctx.execute()
                if ctx.response["data"].get("tts"):
                    ctx.say(ctx.response["data"]["tts"])

    return ctx

def on_exit(ctx):
    ctx.set_config("talk.active", False)