import os, json, subprocess, shutil

def action_data():
    return {
        "name": "appman",
        "author": "Kaiser",
        "version": "0.0",
        "features": [],
        "group": "system",
}
open_file_name = ""

def on_help(ctx):
    return """   

    Commands:
        run <appname>
            Runs the command specified.

        show <appname>
            Shows information on app.

        edit <appname> <key> <value>
            Edits a key in the launcher file.

        list | ls
            Shows all apps.

        rename <oldname> <newname>
            Changes command name.

        delete <appname>
            Deletes command.

        link [--name:<appname>] [--command:<appcommand>]
            Creates new launcher called appname which links to appcommand.

        check [--fix]
            Runs through the application directory and checks if they all have a launcher related to them.
    """

def get_app(ctx, name, *, need_exact = False):
    apps_dir = ctx.data_path()
    if not apps_dir.endswith("/"): apps_dir = apps_dir+"/"
    if not os.path.exists(apps_dir):
        return None
    
    if os.path.exists(apps_dir+name+".json"):
        with open(apps_dir+name+".json", 'r') as f:
            return json.load(f)
    else:
        if need_exact:
            return ctx.writeln("Can't infer selection, requires exact input.")
        out = []
        for filename in os.listdir(apps_dir):
            f = os.path.join(apps_dir, filename)
            if os.path.isfile(f) and filename.endswith(".json") and name.lower() in filename.lower():
                with open(apps_dir+filename, 'r') as f:
                    out.append(json.load(f))
        if len(out) == 1 or ctx.touch_config("appman.select_first", False): return out[0]
        return out

def replaceTags(ctx, string):
    string = string.replace("{ROOT}", ctx.aos_dir)
    string = string.replace("{DATA}", ctx.data_path())
    string = string.replace("{APPS}", os.path.expanduser(ctx.touch_config("appman.dir", "~/.aos_applications/")))
    return string

def launch(ctx, app):
    command = app["command"]
    command = replaceTags(ctx, command)
    extra_args = ctx.get_string_list()[2:]

    wd = app.get("wd", None)

    cwd = os.getcwd()

    if wd != None:
        cwd = os.path.expanduser(wd)
        cwd = replaceTags(ctx, cwd)
        if not os.path.exists(cwd):
            os.makedirs(cwd)
    
    if app.get("generic", False) == True:   
        command = shutil.which(command)

    try:
        p = subprocess.run([command, *extra_args], cwd=cwd)
    except PermissionError:
        ctx.writeln("Permissions error! Updating executable...")
        os.system(f"chmod u+x {command}")
        p = subprocess.run([command, *extra_args], cwd=cwd)
    
    if ctx.touch_config("appman.show_result"): ctx.writeln(f"Application exit: [blue]{p.args}[/blue] (Return code: "+str(p.returncode)+")")

def select_app(ctx, opts):
    for i, opt in enumerate(opts):
        ctx.writeln(f"* ({i}) {opt['name']} ({opt.get('description', 'None')})")
    
    c = input("?> ")

    if c.isdigit() and int(c) < len(opts):
        return opts[int(c)]
    elif c == "":
        return opts[0]
    elif not c.isdigit():
        for opt in opts:
            if c.lower() == opt["name"]:
                return opt
    else:
        return opts[0]

def edit_app(ctx, name, app, key, val):
    apps_dir = ctx.data_path()
    if val == None:
        if app.get(key):    
            del app[key]
        else:
            return ctx.writeln("Key already doesn't exist.")
    else:
        if val.isdigit(): val = int(val)
        elif val == "true" or val == "false": val = bool(val)

        app[key] = val
    with open(apps_dir+name+".json", 'w') as f:
        json.dump(app, f)

def show_app(ctx, app):
    ctx.writeln(f"{app['name']} ({app.get('group', '')})")

    ex = "  * Executes "+replaceTags(ctx, app['command'])
    if app.get("generic"):
        ex += " as "+shutil.which(app['command'])
    if app.get("wd"):
        ex += " in "+replaceTags(ctx, app['wd'])
    ctx.writeln(ex)

def on_load(ctx): 
    apps_dir = ctx.data_path()
    if not os.path.exists(apps_dir):
        os.mkdir(apps_dir)

    cmd = ctx.get_string_ind(0)
    line = ""
    if len(ctx.get_string_list()) > 1:
        line = ctx.get_string_list()[1]
    
    match cmd:
        case "run":
            if line == "": return print("todo error")
            r = get_app(ctx, line)
            if type(r) == dict:
                launch(ctx, r)
            elif type(r) == list:
                launch(ctx, select_app(ctx, r))
        
        case "show":
            if line == "": return print("todo error")
            r = get_app(ctx, line)
            if type(r) == dict:
                show_app(ctx, r)
            elif type(r) == list:
                show_app(ctx, select_app(ctx, r))

        case "edit":
            if line == "": return print("todo error")
            key = ctx.get_string_ind(2)
            val = ctx.get_string_ind(3)
            if val == key: return print("todo error")

            r = get_app(ctx, line, need_exact = True)

            if type(r) == dict:
                edit_app(ctx, line, r, key, val)

            elif type(r) == list:
                rf = select_app(ctx, r)
                edit_app(ctx, line, rf, key, val)

        case "ls" | "list":
            grps = {"default": []}
            #print("---")
            for filename in os.listdir(apps_dir):
                
                f = os.path.join(apps_dir, filename)
                if os.path.isfile(f) and filename.endswith(".json"):
                    with open(apps_dir+filename, 'r') as f:
                        app = json.load(f)
                        if app.get("hidden") == True:
                            continue
                        if app.get("group") == "": app["group"] = "default"
                        if grps.get(app.get("group", "default"), None) == None: grps[app.get("group", "default")] = []
                        grps[app.get("group", "default")].append(app)
                        #show_app(ctx, app)
                        #print("---")
            for key, item in grps.items():
                ctx.writeln(f" --- {key} ---")
                for app in item:
                    show_app(ctx, app)
        
        case "rename":
            oldn = ctx.get_string_ind(1)
            newn = ctx.get_string_ind(2)
            if os.path.exists(apps_dir+oldn+".json") and not os.path.exists(apps_dir+newn+".json"):
                os.rename(apps_dir+oldn+".json", apps_dir+newn+".json")

        case "delete":
            appn = ctx.get_string_ind(1)
            if os.path.exists(apps_dir+appn+".json"):
                os.remove(apps_dir+appn+".json")

        case "link":
            name = ctx.ask("name", prompt="Name of application")
            command = ctx.ask("command", prompt="Command to execute")
            app = {"name": name, 
                    "group": "", 
                    "command": command}
            with open(apps_dir+name+".json", 'w') as f:
                json.dump(app, f)
        
        case "check":
            nolinks = []
            ddir = os.path.expanduser(ctx.touch_config("appman.dir", "~/.aos_applications/"))
            ddir = ddir+"bin/"
            for filename in os.listdir(ddir):
                found = False
                #ctx.writeln(f"Checking {filename}...")

                fullpath = os.path.join(ddir, filename)

                for jsname in os.listdir(apps_dir):
                    
                    with open(apps_dir+jsname, "r") as f:
                        js = json.load(f)
                        realpath = replaceTags(ctx, js["command"])

                        if fullpath == realpath:
                            #ctx.writeln("Exists")
                            found = True
                if not found:
                    nolinks.append(fullpath)

            if len(nolinks) == 0:
                return ctx.writeln("OK")

            if ctx.has_flag("fix"):
                for command in nolinks:
                    
                    name = command.split("/")[-1].split(".")[0].split("-")[0].split("_")[0]
                    ctx.writeln(f"Creating {command} as {name}...")
                    app = {"name": name, 
                            "group": "", 
                            "command": command}
                    with open(apps_dir+name+".json", 'w') as f:
                        json.dump(app, f)

            elif ctx.has_flag("wizard"):
                pass
            else:
                ctx.writeln(f"{len(nolinks)} apps in application directory don't have launchers. Run again with --fix to automatically create launchers, or --wizard to walk through manually.")

                print(nolinks)

    return ctx
