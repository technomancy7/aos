import os

def action_data():
    return {
    "name": "conf",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    pass

def parse_val(line):
    try:
        return eval(line)
    except:
        return line


def on_load(ctx): 
    cmd = ctx.get_string_list()[0]
    line = ctx.get_string_list()[1:]

    conf = ctx.config
    if cmd == "set":
        key = line[0]
        val = " ".join(line[1:])

        if "." in key:
            parent = key.split(".")[0]
            sub = key.split(".")[1]
            if conf.get(parent, None) == None:
                conf[parent] = {}
            
            if type(conf[parent]) == dict:
                conf[parent][sub] = parse_val(val)
                print(f"Key [{parent}.{sub}] set to {conf[parent][sub]} ({type(conf[parent][sub])})")
            else:
                return print("Parent does not accept sub-values.")

        else:
            conf[key] = parse_val(val)
            print(f"Key [{key}] set to {conf[key]} ({type(conf[key])})")

        ctx.save_config()

    elif cmd == "get":
        key = " ".join(line)
        if "." in key:
            parent = key.split(".")[0]
            sub = key.split(".")[1]
            if conf.get(parent, None) == None:
                return print(f"[{parent}.*] is undefined.")
            
            if type(conf[parent]) == dict:
                if conf[parent].get(sub, None) == None:
                    return print(f"[{parent}.{sub}] is undefined")
                print(f"Key [{parent}.{sub}] set to {conf[parent][sub]} ({type(conf[parent][sub])})")
            else:
                return print("Parent does not accept sub-values.")

        else:
            print(f"Key [{key}] set to {conf[key]} ({type(conf[key])})")
    else:
        return print("What?")
    return ctx

def on_exit(ctx):
    print(ctx.exit_code())
