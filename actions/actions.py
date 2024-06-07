import os, importlib, requests, json

class Action:
    @staticmethod
    def __action__():
        return {
        "name": "actions",
        "author": "Kaiser",
        "version": "0",
        "features": [],
        "group": "utility",
    }

    def __help__(self, ctx):
        return """
        Manages internal actions

        Commands:
            new
                - Prompt to create a new action file

            list
                - Shows list of installed actions and info

            download <url>
                - Downloads a python3 script file in to actions directory
                - Downloaded scripts start disabled

            enable/disable <name>
                - Stops AOS from loading or checking that file

            delete <name>
                - Deletes script file and optionally data directory
        """

    def printdata(self, ctx, d):
        comment = ""
        if d["disabled"]: comment = " [red](DISABLED)[/red]"
        if d.get("description"): comment = f"{comment}\n - {d['description']}"
        ctx.writeln(f"[yellow]{d.get('name', 'Unknown')}[/yellow] (v {d.get('version', '0')}) by {d.get('author', '?')} in {d['filename']}{comment}")

    def __run__(self, ctx):
        output = {}
        errors = []

        if ctx.get_string_ind(0) == "new":
            with open(ctx.aos_dir+"action_template.py", "r") as f:
                text = f.read()
                filename = ctx.ask("name", prompt = "Action name?")
                author = ""
                if ctx.touch_config("user.name", "User") != None and ctx.touch_config("user.name", "User") != "User":
                    author = str(ctx.touch_config("user.name"))

                if author == "":
                    author = ctx.ask("author", prompt = "Author name?")

                with open(ctx.aos_dir+"actions/"+filename+".py", "w+") as newact:
                    newact.write(text.replace("$DEFAULT_NAME", filename).replace("$DEFAULT_AUTHOR", author))

        if ctx.get_string_ind(0) == "alias":
            alias = ctx.get_string_ind(1)
            original = ctx.get_string_ind(2)
            if alias == "" and original == "":
                aliases = ctx.touch_config("aliases")
                for k, v in aliases.items():
                    ctx.writeln(f"{k}: {v}")
            else:
                ctx.set_config(f"aliases.{alias}", original)
                ctx.say(f"{alias} is now an alias for {original}.")

        if ctx.get_string_ind(0) == "unalias":
            alias = ctx.get_string_ind(1)
            aliases = ctx.touch_config("aliases")
            del aliases[alias]
            ctx.set_config(f"aliases", aliases)
            ctx.say(f"{alias} is now un-aliased.")

        if ctx.get_string_ind(0) == "enable":
            disabled = ctx.touch_config("system.disabled", [])
            name = ctx.get_string(1)
            if name.lower() in ["system", "conf", "actions"]:
                return ctx.writeln("Can't disable important internal actions.")

            if name in disabled:
                disabled.remove(name)
                ctx.writeln(f"Action {name} enabled.")
                ctx.set_config("system.disabled", disabled)
            else:
                ctx.writeln("Already enabled.")

        if ctx.get_string_ind(0) == "disable":
            disabled = ctx.touch_config("system.disabled", [])
            name = ctx.get_string(1)
            if name not in disabled:
                disabled.append(name)
                ctx.writeln(f"Action {name} disabled.")
                ctx.set_config("system.disabled", disabled)
            else:
                ctx.writeln("Already disabled.")

        if ctx.get_string_ind(0) == "download":
            """Use a dcs manifest system which contains url of script file, name, author, description"""
            url = ctx.get_string(1)
            print(url)
            text = requests.get(url).text
            print(text)
            result = json.loads(text)
            print(result)

        if ctx.get_string_ind(0) == "delete":
            filename = ctx.get_string(1)
            if os.path.exists(ctx.aos_dir+"actions/"+filename+".py"):
                if input(f"Confirm delete of {filename}? Can not be undone. [y/n] > ") == "y":
                    os.remove(ctx.aos_dir+"actions/"+filename+".py")
                    ctx.writeln("Deleting.")
                else:
                    ctx.writeln("Cancelling.")

        if ctx.get_string_ind(0) == "list":
            ctx.update_response(tts = "This is the current available actions.")
            disabled = ctx.touch_config("system.disabled", [])
            show_all = ctx.touch_config("actions.list_disabled") or ctx.has_flag("a")
            directory = ctx.aos_dir+"actions/"

            for filename in os.listdir(directory):
                if filename.endswith(".py"):
                    if filename.split(".")[0] in disabled and not show_all:
                        continue

                    f = os.path.join(directory, filename)
                    if filename == "actions":
                        d = action_data()
                        d["filename"] = filename
                        #printdata(ctx, filename, action_data())
                        if output.get(d.get("group", "default")) == None:
                            output[d.get("group", "default")] = []

                        output[d.get("group", "default")].append(d)

                    if os.path.isfile(f):
                        f = importlib.import_module("actions."+filename.split(".")[0])

                        if hasattr(f, "Action"):
                           #print(f)
                            d = f.Action.__action__()
                            d["filename"] = filename
                            if output.get(d.get("group", "default")) == None:
                                output[d.get("group", "default")] = []
                            d["disabled"] = filename.split(".")[0] in disabled
                            output[d.get("group", "default")].append(d)

                        elif hasattr(f, "action_data"):
                            d = f.action_data()
                            d["filename"] = filename
                            if output.get(d.get("group", "default")) == None:
                                output[d.get("group", "default")] = []
                            d["disabled"] = filename.split(".")[0] in disabled
                            output[d.get("group", "default")].append(d)
                            #printdata(ctx, filename, d)
                        else:
                            errors.append(filename.split(".")[0])
                            #ctx.writeln(f"{filename.split('.')[0]} has no action_data property.", style="dim")

            for key in output.keys():
                ctx.writeln(" = "+key+" =")
                for act in output[key]:
                    self.printdata(ctx, act)

            if len(errors) > 0:
                ctx.writeln(" = Errors =")
                for err in errors:
                    ctx.writeln(f"{err} has no action_data property.", style="dim")
        return ctx
