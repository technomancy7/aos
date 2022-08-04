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
    if type(args) == str: args = shlex.split(args)
    if len(args) == 0: args = ['actions', "list"]

    cmd = args[0]
    lines = args[1:]

    context = Context(command=cmd, lines=lines, base_dir = ATHENAOS_PATH)
    context.load_config()
    context.plaintext_output = context.touch_config("plaintext", False)
    context.execute()
    #print(context.response["data"])
    if context.response["data"].get("tts"):
        context.say(context.response["data"]["tts"])
    #print(context.response)

def run(args):
    try:
        main(args)
    finally:
        if len(context.buffer) != 0:
            with open(context.aos_dir+"self.log", "a+") as f:
                f.write("\n--- NEW LOG START ---\n\n")
                for out in context.buffer:
                    f.write(out)

if __name__ == "__main__":
    run(sys.argv[1:])
