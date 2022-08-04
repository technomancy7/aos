import arrow

def action_data():
    return {
    "name": "journal",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return """
    Commands:
        add | new | write | n

        edit | e <index>

        delete | del | d <index>

        list | ls
    """

def format_entry(ctx, i, entry):
    if entry["edited"] != None:
        body = f"--- ({i}) {entry['created']} (Edited: {entry['edited']}) ---\n"+entry['body']
    else:
        body = f"--- ({i}) {entry['created']} ---\n"+entry['body']

    while "\n" in body:
        body = body.replace("\n", " <br> ")

    for word in body.split(" "):
        if word.startswith("#"):
            body = body.replace(word, "[red]"+word+"[/red]")

    while " <br> " in body:
        body = body.replace(" <br> ", "\n")
        
    return body

def on_load(ctx): 
    cmd = ctx.get_string_ind(0)
    data = ctx.get_data()

    match cmd:
        case "write" | "new" | "add" | "n":
            body = ctx.open_text_editor().strip()
            print(body)
            if body == "":
                return ctx.writeln("No text to add.")

            new_journal = {"body": body, "created": arrow.now().format(ctx.time_format), "edited": None}
            if data.get("entries", None) == None: data["entries"] = []
            data["entries"].append(new_journal)

            ctx.save_data(data)

        case "delete" | "del" | "d":
            ind = ctx.get_string()[len(cmd)+1:]
            if ind.isdigit():
                entry = data["entries"][int(ind)]
                ctx.writeln(format_entry(ctx, ind, entry))
                del data["entries"][int(ind)]
                ctx.save_data(data)
        
        case "edit":
            ind = ctx.get_string()[len(cmd)+1:]
            if ind.isdigit():
                new_body = ctx.open_text_editor(data["entries"][int(ind)]["body"])
                if new_body == "" or new_body == data["entries"][int(ind)]["body"]:
                    return ctx.writeln("No edit made.")
                data["entries"][int(ind)]["body"] = new_body
                data["entries"][int(ind)]["edited"] = arrow.now().format(ctx.time_format)
                ctx.save_data(data)  
                
        case "list" | "ls":
            i = 0
            for entry in data.get("entries", []):
                ctx.writeln(format_entry(ctx, i, entry))
                i += 1
            ctx.writeln("---")

    return ctx

def on_exit(ctx):
    ctx.delete_text_file() 
