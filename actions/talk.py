import os

def action_data():
    return {
    "name": "talk",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    pass

def on_load(ctx): 
    f = ctx.data_path()

    
    ctx.exit_code(0)
    return ctx

def on_exit(ctx):
    print(ctx.exit_code())
