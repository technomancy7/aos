import os, subprocess, textwrap








def list_screens():
    out = []

    try:
        f = subprocess.check_output(["screen", "-ls"]).decode("utf-8").split("\n")
        for proc in f:
            f = proc.split("\t")
            if len(f) > 1:
                out.append({"id": f[1].split('.')[0], "name": f[1].split('.')[1], "start": f[2][1:-1], "status": f[3][1:-1]})
    except subprocess.CalledProcessError:
        return []
    return out
    
def open_screen(name):
    os.system(f"screen -dmS {name}")

def attach_screen(name):
    os.system(f"screen -a -r {name}")
    
def send_to_screen(name, command):
    os.system(f"screen -S {name} -p 0 -X stuff '{command}\n'")

def close_screen(name):
    os.system(f"screen -S {name} -X quit")