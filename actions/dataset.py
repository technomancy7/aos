import arrow

def action_data():
    return {
    "name": "journal",
    "author": "Kaiser",
    "version": "0.0",
    "features": [],
    "group": "wip",
}

def on_help(ctx):
    return """
    Commands to modify the dataset

    Commands:
        add | new | write | n

        edit | e <index>

        delete | del | d <index>
    """

def on_load(ctx): 
    cmd = ctx.get_string_ind(0)
    data = ctx.get_data()

    match cmd:
        case "write" | "new" | "add" | "n":
            pass
    return ctx

def on_exit(ctx):
    ctx.delete_text_file() 
