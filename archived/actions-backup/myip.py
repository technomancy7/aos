from requests import get

def action_data():
    return {
    "name": "myip",
    "author": "Kai",
    "version": "0.0",
    "features": [],
    "group": "",
}

def on_help(ctx):
    return """

    """


def on_load(ctx): 
    ip = get('https://api.ipify.org').text
    ctx.writeln('Your IP address is: {}'.format(ip))
    return ctx

