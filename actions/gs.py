import tools.libgs
import asyncio
def action_data():
    return {
    "name": "gs",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "gaming",
}

#TODO
# Take path/url to file and send it to a configurable command
def on_load(ctx): 
    ctx.load_config()

    game = ctx.get_string_ind(0)
    host = ctx.get_string_ind(1)
    ms = tools.libgs.GSMaster()
    if host == None:
        asyncio.run(ms.get(game))
        ctx.say(f"There are {ms.players} players on {ms.real_total} servers. Here is a list of servers I could find.")
        for server in ms.servers:
            ctx.writeln(f"* {server.hostname} ({server.numplayers}/{server.maxplayers}) @ {server.ip}:{server.hostport}")
    else:
        server = asyncio.run(ms.get_server(host, game))
        ctx.say(f"Here is the server information for {server.hostname}")
        ctx.writeln(f"Host: {server.ip}:{server.hostport}")
        ctx.writeln(f"Players: {server.numplayers}/{server.maxplayers}")
    
    return ctx
