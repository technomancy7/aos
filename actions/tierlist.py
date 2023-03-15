import tools.tierlist as tl

def action_data():
    return {
    "name": "tierlist",
    "author": "Kaiser",
    "version": "0.05",
    "features": [],
    "group": "toys",
}

def on_help(ctx):
    return """

    """
#@todo rewrite simpler

def on_load(ctx): 
    cmd = ctx.get_string_ind(0) 
    ctx.update_response(object_type = cmd)
    datapath = ctx.data_path()
    tier_path = ctx.ask("l", prompt = "Name of tierlist> ")
    if tier_path == "": return ctx.writeln("No list name given.")
    tierlist = tl.Tierlist().from_file(datapath+tier_path+".json")

    match cmd:
        case "addtier" | "at":
            name = ctx.get_string()[len(cmd)+1:]
            if name == "": return ctx.writeln("No name given.")
            index = int(ctx.get_flag("i", -1))
            if index == -1: index = None
            tierlist.add_tier(name, index)

            ctx.update_response(tier_list = tierlist.data, index = index, operation = "add_tier", name = name)
            tierlist.to_file(datapath+tier_path+".json")


        case "addentry" | "ae":
            entry = ctx.get_string()[len(cmd)+1:]
            if entry == "": return ctx.writeln("No entry given.")
            tier = ctx.ask("t", prompt = "Tier")
            if tier == "": return ctx.writeln("No tier given.")
            tierlist.add_to_tier(tier, entry)
            tierlist.to_file(datapath+tier_path+".json")
            ctx.writeln(tierlist.get_tier(tier))
            ctx.update_response(tier_list = tierlist.data, tier = tier, operation = "add_entry", entry = entry)

        case "show":
            ctx.update_response(tier_list = tierlist.data, operation = "show")
            for tier in tierlist.get_order():
                print(tierlist.get_tier(tier))


    return ctx

