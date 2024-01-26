import shlex
from subprocess import Popen
from tools.screen import *

"""
aos daemon ideas
daemon start - starts a process and adds it to a watchlist along with its PID
daemon stop kills a process and removes it from the list (if its in the list)
daemon restart kills and starts

core daemon watches the list of started daemons and checks if a process with that PID is running, if not, start it and set the PID in the list
"""
def action_data():
    return {
    "name": "daemon",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def new_proc(ctx, command, name):
    #f = open(ctx.aos_dir+name+".log", "w+")
    open_screen(name)
    send_to_screen(name, command)

def on_help(ctx):
    pass

def on_load(ctx): 
    cmd = ctx.get_string_ind(0)

    if cmd == "start":
        name = ctx.get_flag("name") or ctx.lines[1]
        to_run = " ".join(ctx.lines[1:])
        if to_run.startswith("self:"):
            to_run = to_run[5:]
            to_run = "python3 "+ctx.aos_dir+"daemons/"+to_run+".py"
        
        new_proc(ctx, to_run, "aos_"+name)

    elif cmd == "list":
        for proc in list_screens():
            if proc["name"].startswith("aos_"):
                print(proc["name"][4:])

    elif cmd == "stop":
        for proc in list_screens():
            if proc["name"].startswith("aos_") and ctx.get_string_ind(1) in proc["name"]:
                print('Stopping '+proc["name"])
                close_screen(proc["name"])
    return ctx
