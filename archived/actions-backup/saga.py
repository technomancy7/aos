import os, json
from tools.datascript import *

def action_data():
    return {
    "name": "saga",
    "author": "Kai",
    "version": "0.0",
    "features": [],
    "group": "",
}

def on_help(ctx):
    return """

    Commands:
        pass
    """

default_story = """
@title Default Title
@author Unknown

start notes
These are notes.
end

start Entites.protagonist
@name Protagonist
end

start Chapters.1
@title Introduction
Text here.
Write your chapter here.
end
"""

def on_load(ctx): 
    cmd = ctx.get_string_at(0)

    match cmd:
        case "write":
            pass

        case "set":
            pass

        case "activate":
            pass
                        
        case "deactivate" | "quit" | "stop" | "q":
            pass

        case "show":
            parser = Datascript()
            story = ctx.get_string()[len(cmd)+1:]
            def globread(ds, line):
                print(f"read block {line}")
            parser.set_fallback("global", globread)

            def block(ds, blockname, line):
                lines = ds.getv(blockname+":lines", [])
                lines.append(line)
                ds.setv(blockname+":lines", lines)

            parser.set_fallback("block", block)
            f = parser.parse_file(ctx.aos_dir+"dsc/stories/"+story+".dsc")
            print(f)

        case "new":
            pass

    return ctx

