import os, json

def action_data():
    return {
    "name": "addrbook",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return """
    Command: add
    Use: Creates new entry in database.
    Options:
        --name:<new name>

    Command: mod
    Use: Modifies entries in database.
    Options:
        --scope:all|<index_name>
        --op:[edit,add,empty,del]
        --field:<field>
        --value:<new value> (Only used for op:edit)
    """

def on_load(ctx): 
    f = ctx.data_path()
    ctx.validate_data_file()
    data = ctx.get_data()
    cmd = ctx.get_string_ind(0)

    if cmd == "add":
        name = ctx.get_flag("name") or input("Name > ")
        if name == "": return print("Name is required.")

        if data.get(name, None) == None:
            data[name] = {}

            ctx.save_data(data)
            print(f"{name} index created.")
            return ctx.exit_code(1)
        else: return print("Index already exists.")

    elif cmd == "mod":
        scope = ctx.get_flag("scope") or input("Scope (Index to add field to) [all] > ")
        field = ctx.get_flag("field") or input("New field > ")
        operation = ctx.get_flag("op") or input("Operation [add, del, edit, empty]> ")
        if operation not in ["add", "edit", "del", "empty"]: return print("Invalid operation.")
        if not field: return print("Field is required.")
        new_value = ""
        if operation == "edit": new_value = ctx.get_flag("value") or input("New value > ")

        if scope == "" or scope == "all":
            if ctx.get_flag("nw") or input("Confirm to alter ALL index (Input y to confirm) > ") == "y":
                for name, index in data.items():
                    #if index.get(field, None) == None:
                    if operation == "empty":
                        index[field] = ""
                    if operation == "del" and index.get(field, None) != None:
                        del index[field]
                    if operation == "add" and index.get(field, None) != None:
                        index[field] = ""
                    if operation == "edit":
                        index[field] = new_value
                ctx.save_data(data)
                return ctx.exit_code(1)
            else:
                print("Cancelled.")
                return ctx.exit_code(0)
        else:
            print(data)
            index = data.get(scope, None)
            if index != None:
                if operation == "empty":
                    index[field] = ""
                if operation == "del" and index.get(field, None) != None:
                    del index[field]
                if operation == "add" and index.get(field, None) != None:
                    index[field] = ""
                if operation == "edit":
                    index[field] = new_value
                print(index)
                ctx.save_data(data)
                return ctx.exit_code(1)
            else:
                return print("Index does not exist.")

    ctx.exit_code(0)
    return ctx

def on_exit(ctx):
    print(ctx.exit_code())
