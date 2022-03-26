import requests 
from textwrap import dedent
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

    q = ""

    if ctx.touch_config("user.post_code", ""):
        q = ctx.touch_config("user.post_code", "")
    if q == "" or ctx.has_flag("loc"):      
        q = ctx.ask("loc", prompt = "Location for query")

    if ctx.has_flag("fc"):
        days = ctx.get_flag("days") or "7"
        url = f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={q}&days={days}&aqi=no&alerts=yes"
        result = requests.get(url).json()
        loc = result['location']
        out = []
        out.append(loc["name"]+' in '+loc["region"]+', '+loc["country"]+' ('+loc["tz_id"]+')')
        days = result['forecast']['forecastday']
        for fday in days:
            day = fday['day']
            precip = []
            if day['daily_will_it_snow'] == 1:
                precip.append(f"{day['daily_chance_of_snow']}% chance of snow.")
            if day['daily_will_it_rain'] == 1:
                precip.append(f"{day['daily_chance_of_rain']}% chance of rain.")
            out.append(dedent(f""" 
                --- {fday['date']} --- 
            Condition: {day['condition']['text']}
            Min: {day['mintemp_c']}c/{day['mintemp_f']}f 
            Avg: {day['avgtemp_c']}c/{day['avgtemp_f']}f 
            Max:{day['maxtemp_c']}c/{day['maxtemp_f']}f
            {' - '.join(precip)}
            """))
        ctx.writeln("\n".join(out))

    elif ctx.has_flag("alerts"):
        days = ctx.get_flag("days") or "7"
        url = f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={q}&days={days}&aqi=no&alerts=yes"
        result = requests.get(url).json()
        alerts = result['alerts']['alert']
        for alert in alerts:
            ctx.writeln(dedent(f""" 
--- {alert['headline']} ({alert['category']}) ---
{alert['event']}
{alert['desc']}
-
{alert['instruction']}

Effective between {alert['effective']} - {alert['expires']}
            """))
    else:
        url = f"http://api.weatherapi.com/v1/current.json?key={key}&q={q}&aqi=no"
        
        result = requests.get(url).json()
        #print(result)
        loc = result['location']
        cur = result['current']
        cond = cur['condition']
        ctx.writeln(dedent(f"""
        {loc["name"]} in {loc["region"]} {loc["country"]} {loc["tz_id"]}
        {cur['temp_c']}c / {cur['temp_f']}f
        {cond['text']}
        """))

    return ctx

