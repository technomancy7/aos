import os

def action_data():
    return {
    "name": "talk",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_load(ctx): 
    f = ctx.app_dir(action_data()["name"])
    if not os.path.exists(f+"data.json"):
        with open(f+"data.json", 'w+') as f:
            f.write("{}")
