import os
from textwrap import dedent

def action_data():
    return {
    "name": "notes",
    "author": "Kaiser",
    "version": "1.0b",
    "features": [],
    "group": "utility",
}

def on_help(ctx):
    return dedent("""
    Commands:
        add <text> --tags:<tag1,tag2...> --group:<group>
        list --tags:<tag1,tag2...> --group:<group> (--hidden)
        edit <new text> --i:<index>
        delete <index>
        group --i:<index> <new group>
        tag --i:<index> --tags:<new tags...>
        addtag --i:<index> tag1,tag2
        untag --i:<index> tag1,tag2
    """)

def format_note(note, *, i = 0):
    ftags = []
    for tag in note['tags']: ftags.append(f"[green]{tag}[/green]")
    pretag = ""
    if len(ftags) > 0: pretag = "\n"
    out = dedent(f"[blue]#[/blue][yellow]{i}[/yellow] @ [yellow]{note['group']}[/yellow]\n{note['text']}{pretag}{' | '.join(ftags)}")

    return out

def on_load(ctx): 
    d = ctx.get_data()
    if d.get("notes", None) == None: d["notes"] = []
    cmd = ctx.get_string_ind(0)
    tags = []
    if ctx.has_flag("tags"): tags = ctx.get_flag("tags").split(",")
    group = ctx.get_flag("group") or "main"

    if cmd == "" or cmd == None: cmd = "list"
    match cmd:
        case "add" | "new":
            note = ""
            if ctx.has_flag("f"):
                note = ctx.open_text_editor().strip()
            else:
                note = ctx.get_string()[len(cmd)+1:]

            if note != "":
                ctx.writeln("Adding note.")
                d["notes"].append({"text": note, "tags": tags, "group": group})
                ctx.save_data(d)
            ctx.delete_text_file() 

        case "list" | "ls":
            hidden = ctx.has_flag("hidden")
            i = 0
            hiddens = 0
            for note in d["notes"]:
                if "hidden" in note["tags"] and hidden == False:
                    hiddens += 1
                else:
                    show = True
                    if len(tags) > 0:
                        show = False
                        if any(x in tags for x in note["tags"]):
                            show = True
                        
                    if show == True and group != "main":
                        show = False
                        if group == note['group']: show = True
                        
                    if show:
                        ctx.writeln("---")
                        ctx.writeln(format_note(note, i=i))
                    else: hiddens += 1
                i += 1

            ctx.writeln("---")
            if hiddens > 0: ctx.writeln(f"{hiddens} hidden notes.")

        case "delete" | "del" | "d":
            index = -1

            #try:
            index = int(ctx.get_string(1))
            if index >= len(d["notes"]):
                return ctx.writeln("Index must be below "+str(len(d['notes'])))
            #except:
                #return ctx.writeln("Invalid selection input.")

            note = d["notes"][index]
            ctx.writeln(format_note(note, i=index))
            d["notes"].remove(note)
            ctx.save_data(d)
            ctx.writeln("!! DELETED !!")


        case "edit":
            index = ctx.get_flag("i") or -1
            if index == -1: return ctx.writeln("Missing: --i:<index to edit>")
            index = int(index)
            note = d["notes"][index]
            new_body = ctx.get_string()[len(cmd)+1:]
            if new_body and new_body != note["text"]: 
                ctx.writeln("Previous: "+note["text"])
                note["text"] = new_body

            ctx.writeln(format_note(note, i=index))
            d["notes"][index] = note
            ctx.save_data(d)

        case "tag":
            index = ctx.get_flag("i") or -1
            if index == -1: return ctx.writeln("Missing: --i:<index to edit>")
            index = int(index)
            note = d["notes"][index]

            if tags != note["tags"]: 
                ctx.writeln("Previous tags: "+' | '.join(note["tags"]))
                note["tags"] = tags

            ctx.writeln(format_note(note, i=index))
            d["notes"][index] = note
            ctx.save_data(d)

        case "addtag":
            index = ctx.get_flag("i") or -1
            if index == -1: return ctx.writeln("Missing: --i:<index to edit>")
            index = int(index)
            note = d["notes"][index]

            tags = ctx.get_string()[len(cmd)+1:].split(",")
            print(tags)
            note["tags"] += tags
            note["tags"] = list(set(note["tags"]))
            ctx.writeln(format_note(note, i=index))
            d["notes"][index] = note
            ctx.save_data(d)

        case "untag":
            index = ctx.get_flag("i") or -1
            if index == -1: return ctx.writeln("Missing: --i:<index to edit>")
            index = int(index)
            note = d["notes"][index]

            tags = ctx.get_string()[len(cmd)+1:].split(",")
            for tag in tags: note["tags"].remove(tag)

            ctx.writeln(format_note(note, i=index))
            d["notes"][index] = note
            ctx.save_data(d)

        case "group":
            group = ctx.get_string()[len(cmd)+1:] or group
            index = ctx.get_flag("i") or -1
            if index == -1: return ctx.writeln("Missing: --i:<index to edit>")
            index = int(index)
            note = d["notes"][index]

            if group != note["group"]: 
                ctx.writeln("Previous group: "+note["group"])
                note["group"] = group

            ctx.writeln(format_note(note, i=index))
            d["notes"][index] = note
            ctx.save_data(d)
    return ctx


