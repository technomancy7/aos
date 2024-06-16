import os, requests
def action_data():
    return {
    "name": "tr",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

def on_load(ctx):
    ctx.load_config()
    mir:str = ctx.touch_config("translate.mirror", "https://libretranslate.de/translate")
    to_translate = ctx.get_string()
    to_lang = ctx.ask("to", default = "en")
    from_lang = ctx.ask("from", default = "auto")
    result = requests.post(mir, data={
        "q": to_translate,
		"source": from_lang,
		"target": to_lang,
		"format": "text"
    })

    text = result.json().get("translatedText", "No result.")
    if ctx.touch_config("talk.active"):
        if ctx.touch_config("translate.short_response", False):
            ctx.say(text)
        else:
            ctx.say(f"{to_translate} translates to {text}")
    else:

        ctx.writeln(f"{to_translate} = {text}")
    return ctx
