import os

def action_data():
    return {
    "name": "shell",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    pass

def on_load(ctx): 

    ctx.exit_code(100)

    while ctx.exit_code(100):
        usr = input("> ")
        

    ctx.exit_code(0)
    return ctx

def on_exit(ctx):
    print(ctx.exit_code())
