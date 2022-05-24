import os, importlib

def action_data():
    return {
    "name": "actions",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return """ 
    Manages internal actions

    Commands:
        new
            - Prompt to create a new action file

        list
            - Shows list of installed actions and info
            
        download <url>
            - Downloads a python3 script file in to actions directory
            - Downloaded scripts start disabled

        enable/disable <name>
            - Stops AOS from loading or checking that file

        delete <name>
            - Deletes script file and optionally data directory
    """

def printdata(ctx, d):
    ctx.writeln(f"[yellow]{d.get('name', d['filename'])}[/yellow] (v {d.get('version', '0')}) by {d.get('author', '?')}")

def on_load(ctx): 
    output = {}
    errors = []
    if ctx.get_string_ind(0) == "list":
        directory = ctx.aos_dir+"actions/"
        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                f = os.path.join(directory, filename)
                if filename == "actions":
                    d = action_data()
                    d["filename"] = filename
                    #printdata(ctx, filename, action_data())
                    if output.get(d.get("group", "default")) == None:
                        output[d.get("group", "default")] = []

                    output[d.get("group", "default")].append(d)
                    
                if os.path.isfile(f):
                    f = importlib.import_module("actions."+filename.split(".")[0])
                    if hasattr(f, "action_data"):
                        d = f.action_data()
                        d["filename"] = filename
                        if output.get(d.get("group", "default")) == None:
                            output[d.get("group", "default")] = []

                        output[d.get("group", "default")].append(d)
                        #printdata(ctx, filename, d)
                    else:
                        errors.append(filename.split(".")[0])
                        #ctx.writeln(f"{filename.split('.')[0]} has no action_data property.", style="dim")

        for key in output.keys():
            ctx.writeln(" = "+key+" =")
            for act in output[key]:
                printdata(ctx, act)

        if len(errors) > 0:
            ctx.writeln(" = Errors =")
            for err in errors:
                ctx.writeln(f"{err} has no action_data property.", style="dim")
    return ctx
