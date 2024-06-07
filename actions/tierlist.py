import os
class Action:
    @staticmethod
    def __action__():
        return {
        "name": "tierlist",
        "author": "Kaiser",
        "version": "0.05",
        "features": [],
        "group": "toys",
    }

    def __help__(self, ctx):
        return """
            A tierlist manager.
        """
    #@todo rewrite simpler

    def __run__(self, ctx):
        #cmd = ctx.get_string_ind(0)
        #name = ctx.get_string_ind(1)
        cmd, name = ctx.cmdsplit()
        d = ctx.data_path()
        if cmd == "": return ctx.writeln("Missing values.")
        match cmd:
            case "ls" | "list" | "lists":
                for filename in os.listdir(d):
                    if filename.endswith(".eno"):
                        ctx.writeln(f":right_arrow: {filename.split('.')[0]}")

            case "show" | "get":
                if name == "": return ctx.writeln("Missing name.")
                data = ctx.get_data_doc(name)
                auth = data.field("author").optional_string_value() or "Unknown"
                tname = data.field("name").optional_string_value() or "Unnamed"
                tdesc = data.field("description").optional_string_value()
                ctx.writeln(f":right_arrow: {tname} by {auth}")
                if tdesc: ctx.writeln(f":right_arrow: {tdesc}")
                for tier in data.section("Tiers").lists():
                    tier_name = tier.string_key()
                    #values =
                    f_values = '\n'.join([f" - {v}" for v in tier.optional_string_values()])
                    ctx.write_panel(f" < {tier_name} >\n\n{f_values}")


            case "edit" | "e":
                if name == "": return ctx.writeln("Missing name.")
                ctx.edit_code(d+name+".eno")


        return ctx
