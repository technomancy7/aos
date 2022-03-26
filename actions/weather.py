import os 
def action_data():
    return {
    "name": "weather",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}


def on_load(ctx): 
    ctx.load_config()
    key = ctx.touch_config("keys.weather", "")
    if key == "":
        return print("Config needed: keys.weather (API key)")

    q = ctx.ask("loc")
    url = f"http://api.weatherapi.com/v1/current.json?key={key}&q={q}&aqi=no"
    


    return ctx

