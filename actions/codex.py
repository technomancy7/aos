import os, json

def action_data():
    return {
    "name": "addrbook",
    "author": "Kaiser",
    "version": "1.0b",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return """
    --db:<database>
        Use a different database name, useful for grouping different entities together

    Commands: 
        list | ls (default)
        Shows all entries

        db <<name>>
        If no name given, lists all database names.
        Else changes active database.

        update | u <entity>.<key> = <value>
        Edits an entry quickly.

        add <name>
        Use: Creates new entity in database.
        Options:
            --name:<new name>

        mod
        Use: Modifies entity/entities in database.
        Options:
            --scope:all|<index_name>
            --op:[edit,add,empty,del]
            --field:<field>
            --value:<new value> (Only used for op:edit)
    """

def pretty_print_entity(ctx, name, entity):
    ctx.writeln(f"[green bold]{name}[/green bold]")
    for k, v in entity.items():
        ctx.writeln(f" * [blue]{k}[/blue] = [yellow]{v}[/yellow]")

def on_load(ctx): 
    f = ctx.data_path()
    ctx.validate_data_file()
    data = ctx.get_data()
    cmd = ctx.get_string_ind(0)

    db = ctx.touch_config("codex.database", "addrbook")
    if ctx.has_flag("db"): 
        db = ctx.get_flag("db")
        ctx.set_config("codex.database", db)
        print("Updated default database record: "+db)

    if data.get(db, None) == None: data[db] = {}

    if cmd == "" or cmd == None: cmd = "list"
    ctx.writeln(f" --- Currently in {db} ---")
    match cmd:
        case "add":
            name = ctx.get_string()[len(cmd)+1:] or ctx.get_flag("name") or input("Name > ")
            if name == "": return print("Name is required.")

            if data[db].get(name, None) == None:
                data[db][name] = {}

                ctx.save_data(data)
                print(f"{name} index created.")
                return ctx.exit_code(1)
            else: return print("Index already exists.")

        case "db":
            new = ctx.get_string()[len(cmd)+1:]
            if new:
                ctx.set_config("codex.database", new)
                ctx.writeln("Updated default database record: "+new)
            else:
                ctx.writeln("Databases:")
                for n, _ in data.items():
                    ctx.writeln(f" [blue]{n}[/blue]")

        case "delete" | "del" | "d":
            name = ctx.get_string()[len(cmd)+1:] or ctx.get_flag("name") or input("Name > ")
            if data[db].get(name, None) != None:
                pretty_print_entity(ctx, name, data[db][name])
                if ctx.get_flag("nw") or input("Confirm to delete (Input y to confirm) > ") == "y":
                    del data[db][name]
                    ctx.save_data(data)
        case "list" | "ls":
            for name, index in data[db].items():
                pretty_print_entity(ctx, name, index)

        case "update" | "u":
            line = ctx.get_string()[len(cmd)+1:]

            if line != "":
                if "." in line and "=" in line:
                    try:
                        entity = line.split(".")[0]
                        key = line.split(".")[1].split("=")[0].strip()
                        value = line.split(".")[1].split("=")[1].strip()
                    except:
                        return ctx.writeln("Problem parsing line format...")
                    if key != "" and entity != "" and value != "":
                        #print(entity, key, value)
                        if data[db].get(entity, None) == None:
                            ctx.writeln("Entity not found.")
                        else:
                            data[db][entity][key] = value
                            pretty_print_entity(ctx, entity, data[db][entity])
                            ctx.save_data(data)

                    else:
                        ctx.writeln("Problem parsing line format...")
                else:
                    ctx.writeln("Problem parsing line format...")
            else:
                ctx.writeln("Invalid or no value given.")
        case "mod":
            scope = ctx.get_flag("scope") or input("Scope (Index to add field to) [all] > ")
            field = ctx.get_flag("field") or input("New field > ")
            operation = ctx.get_flag("op") or input("Operation [add, del, edit, empty]> ")
            if operation not in ["add", "edit", "del", "empty"]: return print("Invalid operation.")
            if not field: return print("Field is required.")
            new_value = ""
            if operation == "edit": new_value = ctx.get_string()[len(cmd)+1:]
            #.get_flag("value") or input("New value > ")

            if scope == "" or scope == "all":
                if ctx.get_flag("nw") or input("Confirm to alter ALL index (Input y to confirm) > ") == "y":
                    for name, index in data[db].items():
                        #if index.get(field, None) == None:
                        if operation == "empty":
                            index[field] = ""
                        if operation == "del" and index.get(field, None) != None:
                            del index[field]
                        if operation == "add" and index.get(field, None) == None:
                            index[field] = ""
                        if operation == "edit":
                            index[field] = new_value
                    ctx.save_data(data)
                    return ctx.exit_code(1)
                else:
                    print("Cancelled.")
                    return ctx.exit_code(0)
            else:
                index = data[db].get(scope, None)
                if index != None:
                    if operation == "empty":
                        index[field] = ""
                    if operation == "del" and index.get(field, None) != None:
                        del index[field]
                    if operation == "add" and index.get(field, None) == None:
                        index[field] = ""
                    if operation == "edit":
                        index[field] = new_value
                    ctx.save_data(data)
                    return ctx.exit_code(1)
                else:
                    return print("Index does not exist.")

    ctx.exit_code(0)
    return ctx
