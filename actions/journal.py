import arrow

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "journal",
            "author": "Kaiser",
            "version": "0",
            "features": [],
            "group": "utility",
        }

    def __gui__(self, sender, app, data):
        #print(data)
        label = data['label']
        context = data['context']
        pos = context.touch_config(f"gui.{label}_pos", [0, 19])
        height = context.touch_config(f"gui.{label}_height", 0)
        width = context.touch_config(f"gui.{label}_width", 0)

        if data["init"](label):
            dpg = data['dpg']
            with dpg.window(label=label, tag=label, pos = pos, width = width, height = height, on_close = lambda: data["close"](label)):
                with dpg.table(header_row=True, row_background=True,
                   borders_innerH=True, borders_outerH=True, borders_innerV=True,
                   borders_outerV=True):

                    dpg.add_table_column(label="Body")
                    dpg.add_table_column(label="Created")
                    dpg.add_table_column(label="Edited")
                    dpg.add_table_column(label="-EDIT-")
                    dpg.add_table_column(label="-DELETE-")

                    def test(a, b, c):
                        print(a, b, c)
                    jd = context.get_data(override="journal")    
                    #print(data)
                    for entry in jd.get("entries", []):    
                        with dpg.table_row():
                            dpg.add_text(f"{entry['body']}")
                            dpg.add_text(f"{entry['created']}")
                            dpg.add_text(f"{entry['edited']}")
                            dpg.add_button(label=f"EDIT", callback=test)
                            dpg.add_button(label=f"DELETE", callback=test)
                                
    def __help__(self, ctx):
        return """
            Commands:
                add | new | write | n

                edit | e <index>

                delete | del | d <index>

                list | ls
            """

    def __run__(self, ctx): 
        cmd = ctx.get_string_ind(0)
        data = ctx.get_data()

        match cmd:
            case "write" | "new" | "add" | "n":
                body = ctx.open_text_editor().strip()
                print(body)
                if body == "":
                    return ctx.writeln("No text to add.")

                new_journal = {"body": body, "created": arrow.now().format(ctx.time_format), "edited": None}
                if data.get("entries", None) == None: data["entries"] = []
                data["entries"].append(new_journal)

                ctx.save_data(data)

            case "delete" | "del" | "d":
                ind = ctx.get_string()[len(cmd)+1:]
                if ind.isdigit():
                    entry = data["entries"][int(ind)]
                    ctx.writeln(self.format_entry(ctx, ind, entry))
                    del data["entries"][int(ind)]
                    ctx.save_data(data)
            
            case "edit":
                ind = ctx.get_string()[len(cmd)+1:]
                if ind.isdigit():
                    new_body = ctx.open_text_editor(data["entries"][int(ind)]["body"])
                    if new_body == "" or new_body == data["entries"][int(ind)]["body"]:
                        return ctx.writeln("No edit made.")
                    data["entries"][int(ind)]["body"] = new_body
                    data["entries"][int(ind)]["edited"] = arrow.now().format(ctx.time_format)
                    ctx.save_data(data)  
                    
            case "list" | "ls":
                i = 0
                for entry in data.get("entries", []):
                    ctx.writeln(self.format_entry(ctx, i, entry))
                    i += 1
                ctx.writeln("---")

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        ctx.delete_text_file() 

    def format_entry(self, ctx, i, entry):
        if entry["edited"] != None:
            body = f"--- ({i}) {entry['created']} (Edited: {entry['edited']}) ---\n"+entry['body']
        else:
            body = f"--- ({i}) {entry['created']} ---\n"+entry['body']

        while "\n" in body:
            body = body.replace("\n", " <br> ")

        for word in body.split(" "):
            if word.startswith("#"):
                body = body.replace(word, "[red]"+word+"[/red]")

        while " <br> " in body:
            body = body.replace(" <br> ", "\n")
            
        return body
