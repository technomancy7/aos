from tools.daemon import *
import time, sys, os
HOME = os.path.expanduser("~")+"/"
ATHENAOS_PATH = HOME+".aos/"
sys.path.append(ATHENAOS_PATH)
from objects import Context

def new_proc(ctx, command, name):
    f = open(ctx.aos_dir+name+".log", "w+")
    p =  Popen(shlex.split(command), stdout=f)
    d = ctx.get_data()

    d["procs"].append({
        "command": command,
        "name": name,
        "stdout": ctx.aos_dir+name+".log",
        "pid": p.pid
    })
    ctx.save_data(d)

if __name__ == "__main__":
    ctx = Context(command = "daemons")
    data = ctx.get_data()
    if data.get("procs", None) == None: 
        data["procs"] = []
        ctx.save_data(data)

    while True:
        data = ctx.get_data()
        ctx.load_config()
        if len(data['procs']) == 0:
            print("No daemons...")
        else:
            print(data['procs'])




        time.sleep(ctx.config.get("daemon_delay", 10))