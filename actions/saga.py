import os, json
def action_data():
    return {
    "name": "saga",
    "author": "Kai",
    "version": "0.0",
    "features": [],
    "group": "",
}

# @todo
# Add a home directory override to store stories in

def on_help(ctx):
    return """

    Commands:
        Global flags: 
            --name:<name> 
                Decides name of story in sub-directory. Uses current directory if omitted.

        new \[entity/chapter] (entity or chapter name)
            * Creates a new story using global name.
            * Creates a new entity or chapter if keyword `entity` or `chapter` are given. Name will be any following text. Story name flag still dictates if using current directory or sub-directory.
        
        show \[chapter/entity (name) | stories] 
            * Shows current story information.
            * If chapter or entity keywords given, shows information of that entity or chapter.
            * if stories keyword given, shows list of seen story directories.

        set <entity.>key [value]
            * Sets entity property.
            * If no entity given, sets story value instead.

        write \[chapter_id]
            * Opens chapter in default text editor.
            * If input is a number, searches for `chapter_<chapter_id>`

        activate \[story id or name]
            * Switches to target stories directory so that all functions run in that stories directory.
            * If number is given, selects based on index shown in `show stories`
            * Else searches by name.
        
        deactivate
            * Resets `activate`
    """

default_story_json = {
  "name": "",
  "author": "",
  "url": "",
  "custom_order": []
}

def is_indexed(ctx, path):
    stories_index = ctx.touch_config("saga.stories", [])
    return path in stories_index

def index(ctx, path):
    if not is_indexed(ctx, path):
        stories_index = ctx.touch_config("saga.stories", [])
        stories_index.append(path)
        ctx.set_config("saga.stories", stories_index)


def on_load(ctx): 
    cmd = ctx.get_string_at(0)
    
    if ctx.touch_config("saga.active"):
        rootdir = ctx.touch_config("saga.active")
    else:
        rootdir = ctx.touch_config("saga.directory", None) or os.getcwd()+"/"
        name = ctx.get_flag("name", "").replace("_", " ")
        rootdir = rootdir+name
        if not rootdir.endswith("/"): rootdir = rootdir+"/"

    match cmd:
        case "index":
            if ctx.get_string(1) == "here":
                here = os.getcwd()+"/"
                if not os.path.exists(here+"story.json"): return ctx.writeln("Invalid story directory.")
                index(ctx, here)
                print("Indexed here.", here)
            else:
                if not os.path.exists(rootdir+"story.json"): return ctx.writeln("Invalid story directory.")
                index(ctx, rootdir)
                print("Indexed root.", rootdir)

        case "write":
            if not os.path.exists(rootdir+"story.json"): return ctx.writeln("Invalid story directory.")
            index(ctx, rootdir)
            chapter = ctx.get_string(1)
            if chapter.isdigit(): chapter = "chapter_"+chapter
            if not os.path.exists(rootdir+"chapters/"+chapter+".md"):
                return ctx.writeln("Chapter not found.")
            #text = ""
            #with open(rootdir+"chapters/"+chapter+".md", "r") as f:
                #current = f.read()
            text = ctx.edit_file(rootdir+"chapters/"+chapter+".md")

            with open(rootdir+"chapters/"+chapter+".md", "w") as f:
                f.write(text)

        case "set":
            if not os.path.exists(rootdir+"story.json"): return ctx.writeln("Invalid story directory.")
            index(ctx, rootdir)
            key = ctx.get_string_at(1)
            val = ctx.get_string(2, default=None)
            print(key, "=", val)
            if key == None: return ctx.writeln("Format: key value")
            if "." in key:
                parent = key.split(".")[0]
                key = key.split(".")[1]
                
                data = {}
                if os.path.exists(rootdir+"entities/"+parent+".json"):
                    with open(rootdir+"entities/"+parent+".json") as f:
                        data = json.load(f)
                    
                data[key] = val

                with open(rootdir+"entities/"+parent+".json", "w") as f:
                    json.dump(data, f)

            else:
                data = {}
                with open(rootdir+"story.json") as f:
                    data = json.load(f)

                data[key] = val

                with open(rootdir+"story.json", "w") as f:
                    json.dump(data, f)

        case "activate":
            ind = ctx.get_string(1)
            if ind == "":
                ctx.writeln("Needs a story id.")
                return

            stories_index = ctx.touch_config("saga.stories", [])

            if ind.isdigit():
                ind = int(ind)
                if ind > len(stories_index): return ctx.writeln("Invalid index.")
                ctx.set_config("saga.active", stories_index[ind])
                ctx.writeln("Activated "+stories_index[ind])
            else:
                for path in stories_index:
                    if ind.lower() in os.path.split(path)[0].split("/")[-1].lower():
                        ctx.writeln("Activated "+path)
                        return ctx.set_config("saga.active", path)
                        
        case "deactivate" | "quit" | "stop" | "q":
            ctx.set_config("saga.active", None)
            ctx.writeln("Deactivated.")   

        case "show":
            something = ctx.get_string_at(1)
            name_of = ctx.get_string_at(2)

            if something == "stories":
                stories_index = ctx.touch_config("saga.stories", [])
                i = 0
                for story in stories_index:
                    ctx.writeln(f'\[{i}] "{story}"')
                    i += 1
                return

            if not os.path.exists(rootdir+"story.json"): return ctx.writeln("Invalid story directory.")
            index(ctx, rootdir)

            if name_of and something:
                match something:
                    case "entity":
                        from rich.syntax import Syntax
                        if os.path.exists(rootdir+"entities/"+name_of+".json"):
                            syntax = Syntax.from_path(rootdir+"entities/"+name_of+".json")
                            ctx.writeln(syntax)    
                        else:
                            return ctx.writeln("Entity "+name_of+" not found.")
                    
                    case "chapter":
                        from rich.markdown import Markdown
                        if name_of.isdigit(): name_of = "chapter_"+name_of
                        if os.path.exists(rootdir+"chapters/"+name_of+".md"):
                            with open(rootdir+"chapters/"+name_of+".md") as f:
                                md = Markdown(f.read())
                                ctx.writeln(md)    
                        else:
                            return ctx.writeln("Entity "+name_of+" not found.")
                return

            with open(rootdir+"story.json") as f:
                d = json.load(f)
                ctx.writeln("Story: "+d.get('name', 'Unknown'))
                ctx.writeln("Author: "+d.get('author', 'Unknown'))
                ctx.writeln("URL: "+d.get('url', 'Unknown'))
                if len(d.get('custom_order', [])) > 0: ctx.writeln("Order: "+d.get('custom_order', 'Unknown'))

            ctx.writeln("")    
            ctx.writeln(" - Chapters - ")
            for file in os.listdir(rootdir+"chapters"):
                filename = os.fsdecode(file)
                ctx.writeln(filename.split(".")[0])

            ctx.writeln("")
            ctx.writeln(" - Entities - ")
            for file in os.listdir(rootdir+"entities"):
                filename = os.fsdecode(file)
                ctx.writeln(filename.split(".")[0])

        case "new":
            s = ctx.get_string_at(1)
            
            if s:
                if not os.path.exists(rootdir+"story.json"): 
                    return ctx.writeln("Invalid story directory.")

                nid = ctx.get_string_at(2)
                index(ctx, rootdir)
                match s:
                    case "entity":
                        if not nid: return ctx.writeln("Entity name required.")
                        if os.path.exists(rootdir+"entities/"+nid+".json"):
                            return ctx.writeln("Entity already exists.")

                        with open(rootdir+"entities/"+nid+".json", 'w+') as f:
                            f.write("{}")
                    case "chapter":
                        if not nid: return ctx.writeln("Chapter name required.")
                        if os.path.exists(rootdir+"chapters/"+nid+".md"):
                            return ctx.writeln("Chapter already exists.")
                        with open(rootdir+"chapters/"+nid+".md", 'w+') as f:
                            f.write("")
                return

            index(ctx, rootdir)    
            if not os.path.exists(rootdir):
                os.makedirs(rootdir)

            with open(rootdir+"story.json", 'w+') as f:
                json.dump(default_story_json, f)

            os.mkdir(rootdir+"chapters/")

            with open(rootdir+"chapters/chapter_1.md", 'w+') as f:
                f.write("")

            os.mkdir(rootdir+"entities/")

            with open(rootdir+"entities/protagonist.json", 'w+') as f:
                f.write("{}")

    return ctx

