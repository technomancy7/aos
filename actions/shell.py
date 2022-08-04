import os, shlex, traceback

def action_data():
    return {
    "name": "shell",
    "author": "Kaiser",
    "version": "0.9",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    pass

def on_load(ctx): 
    ctx.set_config("shell.active", True)
    ctx.touch_config("cwd", os.getcwd()+"/")
    prompt = ctx.touch_config("shell.prompt", "> ")
    print(f"Active in {os.getcwd()}")

    subctx = ctx.clone()
    subctx.exit_code(100)
    subctx.load_config()
    subctx.plaintext_output = ctx.touch_config("plaintext", False)

    while subctx.exit_code() == 100:
        usr = input(prompt)

        if usr == "q" or usr == "quit" or usr == "exit":
            subctx.exit_code(1)
            break

        if usr.startswith(":"):
            line = usr[1:]
            try:
                eval(line, {"ctx": ctx})
            except:
                print(traceback.format_exc())
            continue

        usr = shlex.split(usr)

        if len(usr) == 0: usr = ['system', "actions"]

        cmd = usr[0]
        lines = usr[1:]
        subctx.update(command = cmd, lines = lines)
            
        subctx.execute()
        if subctx.response["data"].get("tts"):
            subctx.say(subctx.response["data"]["tts"])

    ctx.exit_code(0)
    return ctx

def on_exit(ctx):
    ctx.set_config("shell.active", False)
    print(ctx.exit_code())
