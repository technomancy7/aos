import json
from fuzzywuzzy import fuzz, process

def action_data():
    return {
    "name": "define",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return """

    """

def on_load(ctx): 
    fuzzy_min = ctx.get_flag("minmatch") or ctx.touch_config("define.minmatch", 60)
    ctx.set_config("define.minmatch", int(fuzzy_min))
    word = ctx.get_string()
    with open(ctx.data_path("json")+"dictionary.json", "r") as f:
        dictionary = json.load(f)

        for k, v in dictionary.items():
            r = fuzz.ratio(word.upper(), k.upper())
            if r >= int(fuzzy_min):
                ctx.writeln(f"{k} ({r}%): \n\t{v}")

    return ctx

