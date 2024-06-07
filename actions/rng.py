import os, random
import tools.dice
from textwrap import dedent

def action_data():
    return {
    "name": "rng",
    "author": "Kaiser",
    "version": "1.0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return dedent("""
    Commands:

    select <options>
        Comma-separated values.
        
    coin | flip

    num
        Format: min,max | min-max | max

    dice <format>
        Format: (fn)[die]d[sides](+mod)
        Examples: d6 | 2d6 | 2d6+2
    """)

def on_load(ctx):
    cmd = ctx.get_string_ind()
    line = ctx.get_string()[len(cmd)+1:]

    match cmd:
        case "dice":
            if line == "": line = "d6"
            result = tools.dice.prettyRoll(line)

            ctx.write_panel(result)


        case "coin" | "flip":
            r = random.choice(["heads", "tails"])
            ctx.write_panel(r)
            ctx.update_response(tts = f"You flipped a {r}")

        case "choice" | "choose" | "select":
            opts = line.split(",")
            opts = [opt.strip() for opt in opts]

            random.shuffle(opts)
            ctx.write_panel(f"Random selection from: {', '.join(opts)}:\n -> {random.choice(opts)}")


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

            ctx.write_panel(str(random.randint(s, e)))

    return ctx
