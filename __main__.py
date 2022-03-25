import os, sys, shlex, json, textwrap
import importlib
from objects import Context
HOME = os.path.expanduser("~")+"/"
ATHENAOS_PATH = HOME+".aos/"
sys.path.append(ATHENAOS_PATH+"modules/")

# TODO
"""
Port over Athena Desktop functionality and apps to here
Maybe keep both, but have this as a cli-only version with slightly different functionality

Usage:

aos <sub-command> <args>
aos talk How are you?


This passes "How are you?" string to the action talk
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
    #args = list(map(editarg,  args))
    if len(args) == 0: args = ['help']
    cmd = args[0]
    lines = args[1:]
    line = " ".join(lines)

    context = Context(command=cmd, line=line, lines=lines)
    context.aos_dir = ATHENAOS_PATH
    context.load_config()
    
    if not os.path.exists(ATHENAOS_PATH+"actions/"+cmd+".py"):
        return print("Action not found")


    f = importlib.import_module("actions."+cmd)
    
    if context.get_flag("help"):
        if hasattr(f, "on_help") and type(f.on_help(context)) == str:
            return print(textwrap.dedent(f.on_help(context)))
        return print(cmd+" has no help.")
    if hasattr(f, "on_load"):
        context = f.on_load(context) or context

    if hasattr(f, "on_exit"):
        f.on_exit(context)

if __name__ == "__main__":
    main(sys.argv[1:])