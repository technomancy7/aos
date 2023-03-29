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
        Globals: --l:<list name>

        addtier | at <name>
        removetier | rt <name
        addentry | a <name> [--t:<tier>]
        removeentry | r <name> [--t:<tier>]
        show
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
            ctx.writeln(f"Tier added. {[t['name'] for t in tierlist.data['tiers']]}")

        case "remove" | "rt":
            name = ctx.get_string()[len(cmd)+1:]
            if name == "": return ctx.writeln("No name given.")
            index = int(ctx.get_flag("i", -1))
            if index == -1: index = None
            tierlist.remove_tier(name)

            ctx.update_response(tier_list = tierlist.data, index = index, operation = "remove_tier", name = name)
            tierlist.to_file(datapath+tier_path+".json")
            ctx.writeln(f"Tier removed. {[t['name'] for t in tierlist.data['tiers']]}")

        case "addentry" | "a":
            entry = ctx.get_string()[len(cmd)+1:]
            if entry == "": return ctx.writeln("No entry given.")
            tier = ctx.ask("t", prompt = "Tier")
            if tier == "": return ctx.writeln("No tier given.")
            tierlist.add_to_tier(tier, entry)
            tierlist.to_file(datapath+tier_path+".json")
            ctx.writeln(f"Tier {tier} updated; {tierlist.get_tier(tier)}")
            ctx.update_response(tier_list = tierlist.data, tier = tier, operation = "add_entry", entry = entry)

        case "removeentry" | "r":
            entry = ctx.get_string()[len(cmd)+1:]
            if entry == "": return ctx.writeln("No entry given.")
            tier = ctx.ask("t", prompt = "Tier")
            if tier == "": return ctx.writeln("No tier given.")
            tierlist.remove_from_tier(tier, entry)
            tierlist.to_file(datapath+tier_path+".json")
            ctx.writeln(f"Tier {tier} updated; {tierlist.get_tier(tier)}")
            ctx.update_response(tier_list = tierlist.data, tier = tier, operation = "add_entry", entry = entry)

        case "show":
            ctx.update_response(tier_list = tierlist.data, operation = "show")
            for tier in tierlist.get_order():
                print(tierlist.get_tier(tier))


    return ctx

