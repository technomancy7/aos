from ast import parse
import os

def action_data():
    return {
    "name": "conf",
    "author": "Kaiser",
    "version": "1.0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return """
    Commands:
        set <<parent.>key> <value>
        get <<parent.>key>
        append <<parent.>key> <value>
        unappend <<parent.>key> <value>
        unset <<parent.>key>
        list
    
    """

def parse_val(line):
    try:
        return eval(line)
    except:
        return line


def on_load(ctx): 
    cmd = ""
    line = []
    if ctx.get_string() == "": 
        cmd = "list"
        
    else:
        cmd = ctx.get_string_list()[0]
        line = ctx.get_string_list()[1:]
    ctx.update_response(operator = cmd)
    conf = ctx.config
    if cmd == "set":
        key = line[0]
        val = parse_val(" ".join(line[1:]))

        ctx.set_config(key, val)
        ctx.writeln(f"[yellow]{key}[/yellow] = [green]{val}[/green] ({type(val)})")
        ctx.update_response(key = key, value = val)
        ctx.save_config()

    elif cmd == "unset":
        key = line[0]
        val = parse_val(" ".join(line[1:]))

        ctx.unset_config(key)
        ctx.writeln(f"[yellow]{key}[/yellow] = [green]None[/green] (None)")
        ctx.update_response(key = key)
        ctx.save_config()

    elif cmd == "unappend":
        key = line[0]
        line = parse_val(" ".join(line[1:]))
        ls = ctx.touch_config(key, None)
        if type(ls) == list:
            ls.remove(line)
            ctx.set_config(key, ls)
            ctx.writeln(f"[yellow]{key}[/yellow] = [green]{ls}[/green] ({type(ls)})")
            ctx.update_response(key = key, value = ls)
        else:
            return ctx.writeln(f"Invalid type for {line}. Expected {type([])}, got {type(ls)}.")

    elif cmd == "append":
        key = line[0]
        line = parse_val(" ".join(line[1:]))
        ls = ctx.touch_config(key, None)
        if type(ls) == list:
            ls.append(line)
            ctx.set_config(key, ls)
            ctx.writeln(f"[yellow]{key}[/yellow] = [green]{ls}[/green] ({type(ls)})")
            ctx.update_response(operator = "append", key = key, value = ls)
        elif type(ls) == str:
            ls += line
            ctx.set_config(key, ls)
            ctx.writeln(f"[yellow]{key}[/yellow] = [green]{ls}[/green] ({type(ls)})")
            ctx.update_response(operator = "append", key = key, value = ls)
        else:
            return ctx.writeln(f"Invalid type for {line}. Expected {type([])} or {type('')}, got {type(ls)}.")

    elif cmd == "get":
        key = " ".join(line)
        val = ctx.touch_config(key, "", ignore = True)
        ctx.update_response(operator = "get", key = key, value = val)
        ctx.writeln(f"[yellow]{key}[/yellow] = [green]{val}[/green] ({type(val)})")

    elif cmd == "list":
        ind = False
        for k, v in conf.items():
            if type(v) == dict:
                ind = True
                ctx.writeln()
                ctx.writeln(f"[blue]{k}[/blue]:")
                for sk, sv in v.items(): 
                    ctx.writeln(f"- [yellow]{sk}[/yellow] = [green]{sv}[/green] ({type(sv)})")
            elif type(v) == list:
                ind = True
                ctx.writeln()
                ctx.writeln(f"[blue]{k}[/blue]:")
                for item in v:
                    ctx.writeln(f"* [yellow]{item}[/yellow] ({type(item)})")
            else:
                if ind:
                    ctx.writeln()
                    ind = False
                ctx.writeln(f"[yellow]{k}[/yellow] = {v} ({type(v)}")
    else:
        return ctx.writeln("What?")
    return ctx
