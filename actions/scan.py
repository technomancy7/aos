import os

def action_data():
    return {
    "name": "scan",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return """
    Commands:

    
    """

def run_dir(ctx, path, depth = 0, *, max_depth = 1, line = "", case_sensitive = False, filetypes = []):
    if depth >= max_depth: return

    for file in os.listdir(path):
        filename = os.fsdecode(file)
        realpath = os.getcwd()+"/"+filename
        if os.path.islink(realpath): continue

        if os.path.isdir(realpath):
            if ctx.has_flag("v"): print(f"Entering sub-directory {realpath}")
            run_dir(ctx, path, depth+1)
        else:
            if filename.endswith(tuple(filetypes)):
                if ctx.has_flag("v"): print(f"Entering file {realpath}")
                with open(realpath, "r") as f:
                    text = f.read().split("\n")
                    for fline in text:
                        if (case_sensitive and line.lower() in fline.lower() ) or (line in fline):
                            ctx.writeln(f"Line {text.index(fline)} in [yellow]{filename}[/yellow]")
                            ctx.writeln(fline)
                continue

    if ctx.has_flag("v"): print(f"Leaving sub-directory {path}")
    
def on_load(ctx): 
    exts = ctx.touch_config("scan.ext", [".txt", ".js", ".uc", ".c", ".cpp", ".h", ".lua", ".rb", ".jl"])
    line = ctx.get_string()
    depth = int(ctx.get_flag("d", 1))
    case_sensitive = ctx.coerce_bool(ctx.get_flag("c", False))
    run_dir(ctx, os.getcwd(), 0, max_depth = depth, line = line, case_sensitive = case_sensitive, filetypes = exts)

    return ctx
