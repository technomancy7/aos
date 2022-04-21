import os, shlex, importlib, textwrap

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

        usr = shlex.split(usr)

        if len(usr) == 0: usr = ['system', "actions"]

        cmd = usr[0]
        lines = usr[1:]
        subctx.update(command = cmd, lines = lines)
            
        subctx.execute()

    ctx.exit_code(0)
    return ctx

def on_exit(ctx):
    ctx.set_config("shell.active", False)
    print(ctx.exit_code())
