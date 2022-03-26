import os, requests
def action_data():
    return {
    "name": "stream",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

#TODO
# Take path/url to file and send it to a configurable command
def on_load(ctx): 
    ctx.load_config()
    mir:str = ctx.touch_config("translate.mirror", "https://libretranslate.de/translate")
    to_translate = ctx.get_string()
    to_lang = ctx.ask("to")
    from_lang = ctx.ask("from")
    result = requests.post(mir, data={		
        "q": to_translate,
		"source": from_lang,
		"target": to_lang,
		"format": "text"
    })

    print(result.json().get("translatedText", "No result."))
    return ctx
