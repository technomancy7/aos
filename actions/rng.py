import os, random
import tools.dice
from textwrap import dedent

def action_data():
    return {
    "name": "rng",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return dedent("""
    Commands:

    coin | flip

    num 
        Format: min,max | min-max | max

    dice
        Format: (fn)[die]d[sides](+mod)
        Examples: d6 | 2d6 | 2d6+2   
    """)

def on_load(ctx): 
    cmd = ctx.get_string_ind()
    line = ctx.get_string()[len(cmd)+1:]

    match cmd:
        case "listadd" | "addlist" | "als" | "lsa":
            listname = ctx.get_flag("l") or "main"
            d = ctx.get_data()
            if d.get("lists", None) == None: d["lists"] = {}
            if d["lists"].get(listname, None) == None: d["lists"][listname] = []
            if line not in d["lists"][listname]:
                d["lists"][listname].append(line)
                ctx.writeln("Added entry "+line+" to "+listname)
                ctx.save_data(d)
            else:
                ctx.writeln(f"{line} already in list {d['lists'][listname]}")

        case "listget" | "getlist" | "gls" | "lsg":
            d = ctx.get_data()
            ln = ctx.get_flag("l") or "main"
            if d.get("lists", None) == None: return ctx.writeln("List does not exist.")
            if d["lists"].get(ln, None) == None: return ctx.writeln("List does not exist.")
            ls = d["lists"][ln]
            ctx.writeln(random.choice(ls))

        case "listshow" | "lss" | "ls" | "list":
            d = ctx.get_data()
            ln = ctx.get_flag("l") or "main"
            if d.get("lists", None) == None: return ctx.writeln("List does not exist.")
            if d["lists"].get(ln, None) == None: return ctx.writeln("List does not exist.")
            ls = d["lists"][ln]
            ctx.writeln(f" --- {ln} ---")
            ctx.writeln(" | ".join(ls))
            
        case "dice":
            if line == "": line = "d6"
            ctx.writeln(tools.dice.prettyRoll(line))

        case "coin" | "flip":
            ctx.writeln(random.choice(["heads", "tails"]))


        case "choice" | "choose" | "select":
            opts = line.split(" ")
            using_spaces = False
            for opt in opts:
                if " " in opt:
                    using_spaces = True

            
            if using_spaces and "|" not in " ".join(opts) and "," not in " ".join(opts):
                opts = list(opts)
                random.shuffle(opts)
                ctx.writeln(f"Random selection from {opts} = {random.choice(opts)}")

            else:
                line = " ".join(opts)
                if "|" in line:
                    opts = line.split("|")
                    ctx.writeln(f"Random selection from {opts} = {random.choice(opts)}")
                elif "," in line:
                    opts = line.split(",")
                    ctx.writeln(f"Random selection from {opts} = {random.choice(opts)}")
                else:
                    opts = line.split(" ")
                    ctx.writeln(f"Random selection from {opts} = {random.choice(opts)}")

        case "num":
            s = 0
            e = 100

            if "," in line:
                s = int(line.split(",")[0])
                e = int(line.split(",")[1])

            elif "-" in line:
                s = int(line.split("-")[0])
                e = int(line.split("-")[1])
            elif line.isdigit():
                e = int(line)

            ctx.writeln(random.randint(s, e))

    return ctx

