import os, sys, shlex, json, textwrap
import importlib

HOME = os.path.expanduser("~")+"/"
ATHENAOS_PATH = HOME+".aos/"
sys.path.append(ATHENAOS_PATH+"lib/")
from objects import Context
context = None
# TODO
"""
Talk mode action using basic regex natural language to pass to commands
Have aliases for common patterns 
So instead of 
Roll a (full dice notation syntax detection) 
Roll a (:dice_notation:) 

Class with dot Learn() 
Detect if passed arg is a dir or file

Tamagotchi style pet
When creating new pet, it populates a pets thing in codex

Use codex addrbook for user and bot to store info for other actions like location for weather
Make sure ctx get data can override without changing own command
"""
def editarg(x):
    prefix = 0
    if x.startswith("--"): prefix = 2
    elif x.startswith("-"): prefix = 1
    out = x.replace("-", " ")
    out = out[prefix:]
    if prefix > 0: out = "-"*prefix+out
    return out 


def main(args):
    global context
    #args = list(map(editarg,  args))
    if len(args) == 0: args = ['help']
    cmd = args[0]
    lines = args[1:]
    line = " ".join(lines)

    context = Context(command=cmd, line=line, lines=lines)
    context.aos_dir = ATHENAOS_PATH
    context.load_config()
    cmd = context.resolve_alias()
    context.plaintext_output = context.touch_config("plaintext", False)
    #aliases = context.touch_config("aliases", {})

    if not os.path.exists(ATHENAOS_PATH+"actions/"+cmd+".py"):
        return print(f"Action {cmd} not found")


    f = importlib.import_module("actions."+cmd)
    
    if context.get_flag("help") or context.get_flag("h"):
        if hasattr(f, "on_help") and type(f.on_help(context)) == str:
            return print(textwrap.dedent(f.on_help(context)))
        return print(cmd+" has no help.")

    if hasattr(f, "on_load"):
        context = f.on_load(context) or context

    if hasattr(f, "on_exit"):
        f.on_exit(context)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    finally:
        if len(context.buffer) != 0:
            with open(context.aos_dir+"self.log", "a+") as f:
                f.write("\n--- NEW LOG START ---\n\n")
                for out in context.buffer:
                    f.write(out)