import os, requests
def action_data():
    return {
    "name": "tr",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}

#TODO
# Take path/url to file and send it to a configurable command
def open_gui(sender, app, data):
    label = data['label']
    context = data['context']
    pos = context.touch_config(f"gui.{label}_pos", [0, 19])
    height = context.touch_config(f"gui.{label}_height", 0)
    width = context.touch_config(f"gui.{label}_width", 0)

    if data["init"](label):

        dpg = data['dpg']
        print("Translator")
        with dpg.window(label=label, tag=label, pos = pos, width = width, height = height, on_close = lambda: data["close"](label)):
            def send_talk(**args):
                pass#print(dpg.get_value("translator_input"))

            #with dpg.group():
            with dpg.group(horizontal=True, width=-1):
                dpg.add_input_text(tag="trlangfrom", width=-1)
                dpg.add_input_text(tag="trlangto", width=-1)
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="trtextfrom", width=-50, multiline=True)
                dpg.add_input_text(tag="trtextto", width=-50, multiline=True)
            dpg.add_button(callback=send_talk, label="Translate")

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
