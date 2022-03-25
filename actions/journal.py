import os

def action_data():
    return {
    "name": "journal",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    pass

def on_load(ctx): 

    return ctx

def on_exit(ctx):
    print(ctx.exit_code())
