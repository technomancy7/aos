import os

def action_data():
    return {
    "name": "cd",
    "author": "Kaiser",
    "version": "1.0",
    "features": [],
    "group": "system",
}

def on_help(ctx):
    return """    
    """


def on_load(ctx): 
    if ctx.touch_config("shell.active", False):
        if ctx.get_string() == "": 
            os.chdir(os.path.expanduser('~'))
            return
            
        os.chdir(os.path.expanduser(ctx.get_string()))
    else: print("Not available.")
    
    return ctx
