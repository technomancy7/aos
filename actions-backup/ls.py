import os, pathlib
from humanfriendly import format_size
def action_data():
    return {
    "name": "ls",
    "author": "Kaiser",
    "version": "1.0",
    "features": [],
    "group": "system",
}

def on_help(ctx):
    return """

    Flags:
        -o:<order>
            Any of `link`, `dir` or `file` seperated by comma.
            Dictates the order that listed objects are shown in.
            Can exclude types of objects by not including that name.
            E.g. just using -o:file will only show files

        -l:<length>
            Max length of name to display
    """


def spacing(word, max = 20):
    if len(word) > max-3: return word[0:max-3]+"..."
    return f"{word}{' '*(max-len(word))}"

def on_load(ctx): 
    order = ["dir", "link", "file"]
    if ctx.has_flag("o"):
        order = ctx.get_flag("o").split(",")
    output = {}
    output["dir"] = []
    output["link"] = []
    output["file"] = []
    max_filename = int(ctx.get_flag("l", 20))+3
    for file in os.listdir(os.getcwd()):
        filename = os.fsdecode(file)

        if os.path.islink(os.getcwd()+"/"+filename):
            realpath = str(os.readlink(os.getcwd()+"/"+filename))
            print(os.getcwd()+"/"+filename)
            print(realpath)
            if os.path.exists(realpath):
                size = os.path.getsize(realpath)
                size = format_size(size, binary=True)
                output["link"].append("link | "+spacing(filename, max_filename)+" | "+size+" ("+realpath+")")
            else:
                output["link"].append("link | "+spacing(filename, max_filename)+" | invalid link")
        elif os.path.isdir(os.getcwd()+"/"+filename): 
            output["dir"].append("dir  | "+spacing(filename, max_filename)+" | N/A")
            continue
        else:
            size = os.path.getsize(os.getcwd()+"/"+filename)
            size = format_size(size, binary=True)
            output["file"].append("file | "+spacing(filename, max_filename)+" | "+size)
            continue
    
    for ord in order:
        for line in output[ord]:
            ctx.writeln(line)
    return ctx
