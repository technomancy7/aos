import os, sys
import importlib

HOME = os.path.expanduser("~")+"/"
ATHENAOS_PATH = HOME+".aos/"
sys.path.append(ATHENAOS_PATH+"modules/")

# TODO
"""
Port over Athena Desktop functionality to here
Maybe keep both, but have this as a cli-only version with slightly different functionality

Usage:

aos <sub-command> <args>
aos talk How are you?


This passes "How are you?" string to the action talk
"""

# Container for generic AOS functions to pass to the context
class AOS:
    def __init__(self):
        self.config = {}

    def load_config(self):
        pass

    def save_config(self):
        pass

class Context:
    def __init__(self, *, aos = None, command = "", line = ""):
        self.aos_dir = ATHENAOS_PATH
        self.command = command
        self.line = line
        self.aos = aos

    def app_dir(self, override = ""):
        name = self.command
        if override != "": name = override
        path = self.aos_dir+"data/"+name+"/"
        if not os.path.exists(path):
            os.makedirs(path)
        return path

def main(args):
    cmd = args[0]
    line = " ".join(args[1:])
    print(cmd, "+", line)
    if not os.path.exists(ATHENAOS_PATH+"actions/"+cmd+".py"):
        return print("Action not found")

    aos = AOS()
    aos.load_config()

    f = importlib.import_module("actions."+cmd)
    context = Context(aos = aos, command=cmd, line=line)

    if hasattr(f, "on_load"):
        f.on_load(context)

    if hasattr(f, "on_exit"):
        f.on_exit(context)

if __name__ == "__main__":
    main(sys.argv[1:])