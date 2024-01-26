import os 
def action_data():
    return {
    "name": "stream",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

#TODO
# Take path/url to file and send it to a configurable command
def on_load(ctx): 
    ctx.load_config()
    cmdln = ctx.touch_config("apps.audio", "vlc '$P'")
    url = ctx.get_string_ind(0)
    os.system(cmdln.replace("$P", url))
    return ctx

def on_exit(ctx):
    print("Stream ended.")
