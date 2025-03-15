import os, json
import webbrowser
import random
import tomlkit
import tomlkit.items

class Action:
    @staticmethod
    def __action__():
        return {
        "name": "codex",
        "author": "Kaiser",
        "version": "1.0b",
        "features": [],
        "group": "utility",
    }

    def __help__(self, ctx):
        return """
        Commands:
            info
            Shows database info

            edit | write | e | w <<db>>
            Opens document for the database in code editor

            search | s <<key>>[ = <<value>>]
            Shows entries which contain a <<key>> and <<value>> match
            If value is "." or empty, shows all entries which contains the key with any value

            set <<db>>.<<entry>>[.<<key>>] = <<value>>
            Sets entry key to value. Value is evaluated to supported datatypes, string by default. Key is `text` if not defined.

            get [<<db>>].<<name>>
            Shows entry with matching <<name>>
                --open:<<field>> - Opens field in browser if it is a valid URL

            list | ls (default)
            Shows all entries

        Special values:
            Entry:
            "hidden from search" = false
            "hidden from list" = false
            list = ["x striked out value", "normal value"]
            display_timespan = "@ 21st of May, 2068"

            File:
            [__aos__]
            "hidden from list" = false
        """

    def get_display_name(self, ctx, name, db = "addrbook"):
        doc = ctx.get_data(db, override="codex", fmt="toml") # override since this function may be called remotely
        return doc.get(name).get("Display Name")

    def __run__(self, ctx):
        #cmd = ctx.get_string_ind(0)
        cmd, ln = ctx.cmdsplit()

        if cmd == "" or cmd == None: cmd = "list"

        match cmd:
            case "info":
                for filename in os.listdir(ctx.data_path()):
                    dbname = filename.split(".")[0]
                    doc = ctx.get_data(dbname, fmt='toml')
                    text = f"{dbname}"
                    i = 0
                    for _ in doc.keys():
                        i += 1
                    text += f" [blue]{i} entries[/blue]"
                    if doc.get("_aos_", {}).get("hidden from list"):
                        text += " (Hidden: _aos_ value)"
                    if dbname in ctx.touch_config("codex.ignores", []):
                        text += " (Hidden: System config)"
                    ctx.writeln(text)


            case "edit" | "write" | "e" | "w":
                if ln:
                    if os.path.exists(ctx.data_path()+ln+".toml"):
                        ctx.writeln("Opening "+ctx.data_path()+ln+".toml")
                        ctx.edit_code(ctx.data_path()+ln+".toml")
                    else:
                        ctx.writeln("DB does not exist.")
                else:
                    files = [f.split(".")[0] for f in os.listdir(ctx.data_path())] + ["Cancel"]
                    opt = ctx.g.choose("Edit which file?", *files)
                    if opt and opt != "Cancel":
                        ctx.writeln("Opening "+ctx.data_path()+opt+".toml")
                        ctx.edit_code(ctx.data_path()+opt+".toml")

            case "search" | "sr":
                for filename in os.listdir(ctx.data_path()):
                    dbname = filename.split(".")[0]
                    doc = ctx.get_data(dbname, fmt='toml')
                    searchstr = ctx.get_string()[len(cmd)+1:]
                    if "=" not in ln:
                        k = ln
                        v = ""
                    else:
                        k = ln.split("=")[0].strip()
                        v = ln.split("=")[1].strip() or ""

                    for ik, iv in doc.items():
                        if not iv.get("hidden from search"):
                            if v == "." or v == "":
                                if iv.get(k) and iv.get(k).lower() != "":
                                    self.pretty_print_entity(ctx, ik, iv, dbname)

                            elif iv.get(k, "").lower() == v.lower():
                                self.pretty_print_entity(ctx, ik, iv, dbname)

            case "unappend" | "uap":
                v = ctx.stdinrd or ln

                if v.count("=") == 0: return ctx.writeln("Format invalid, need: db.entry[.key] = value")
                pointer = v.split("=")[0].strip()
                v = ".".join(v.split("=")[1:]).strip()
                if pointer.count(".") < 1 or pointer.count(".") > 2: return ctx.writeln("Format invalid, need: db.entry[.key] = value")
                db = pointer.split(".")[0]
                name = pointer.split(".")[1]

                if pointer.count(".") == 1: key = "text"
                if pointer.count(".") == 2: key = pointer.split(".")[2]

                data = ctx.get_data(db, fmt="toml")

                if data == None: data = {}
                if not data.get(name): data[name] = {}
                if not data[name].get(key): return ctx.writeln("Key does not exist.")

                if type(data[name][key]) == tomlkit.items.Array:
                    data[name][key].remove(v)
                    ctx.writeln(f":right_arrow: [blue]{db}[/blue].[blue]{name}[/blue].[blue]{key}[/blue] = [green]{data[name][key]}[/green] ({type(v).__name__})")
                else:
                    return ctx.writeln("Value is not appendable.")
                ctx.save_data(data, db, fmt="toml")

            case "append" | "ap":
                v = ctx.stdinrd or ln

                if v.count("=") == 0: return ctx.writeln("Format invalid, need: db.entry[.key] = value")
                pointer = v.split("=")[0].strip()
                v = ".".join(v.split("=")[1:]).strip()
                if pointer.count(".") < 1 or pointer.count(".") > 2: return ctx.writeln("Format invalid, need: db.entry[.key] = value")
                db = pointer.split(".")[0]
                name = pointer.split(".")[1]

                if pointer.count(".") == 1: key = "text"
                if pointer.count(".") == 2: key = pointer.split(".")[2]

                data = ctx.get_data(db, fmt="toml")

                if data == None: data = {}
                if not data.get(name): data[name] = {}
                if not data[name].get(key): return ctx.writeln("Key does not exist.")

                if type(data[name][key]) == tomlkit.items.String:
                    data[name][key] = data[name][key] + v
                    data[name][key] = data[name][key].replace("<br>", "\n")
                    ctx.writeln(f":right_arrow: [blue]{db}[/blue].[blue]{name}[/blue].[blue]{key}[/blue] = [green]{data[name][key]}[/green] ({type(v).__name__})")

                elif type(data[name][key]) == tomlkit.items.Array:
                    data[name][key].append(v)
                    ctx.writeln(f":right_arrow: [blue]{db}[/blue].[blue]{name}[/blue].[blue]{key}[/blue] = [green]{data[name][key]}[/green] ({type(v).__name__})")
                else:
                    return ctx.writeln("Value is not appendable.")

                ctx.save_data(data, db, fmt="toml")

            case "set" | "s":
                v = ctx.stdinrd or ln

                if v.count("=") == 0: return ctx.writeln("Format invalid, need: db.entry[.key] = value")
                pointer = v.split("=")[0].strip()
                v = ".".join(v.split("=")[1:]).strip()
                if pointer.count(".") < 1 or pointer.count(".") > 2: return ctx.writeln("Format invalid, need: db.entry[.key] = value")
                db = pointer.split(".")[0]
                name = pointer.split(".")[1]

                if pointer.count(".") == 1: key = "text"
                if pointer.count(".") == 2: key = pointer.split(".")[2]

                try: v = ctx._safe_eval(v)
                except: pass

                ctx.writeln(f":right_arrow: [blue]{db}[/blue].[blue]{name}[/blue].[blue]{key}[/blue] = [green]{v}[/green] ({type(v).__name__})")

                data = ctx.get_data(db, fmt="toml")

                if data == None: data = {}

                if not data.get(name): data[name] = {}

                data[name][key] = v

                ctx.save_data(data, db, fmt="toml")

            case "get" | "g":
                ent = None
                db = ""
                name = ""
                if "." in ln:
                    db = ln.split(".")[0]
                    name = ln.split(".")[1]
                    doc = ctx.get_data(db, fmt='toml')
                    for k, v in doc.items():
                        if name.lower() == k.lower():
                            ent = doc[name]
                            name = ln.split(".")[1]
                else:
                    for filename in os.listdir(ctx.data_path()):
                        db = filename.split(".")[0]
                        doc = ctx.get_data(db, fmt="toml")
                        for entity in doc.keys():
                            if ln.lower() == entity.lower():
                                ent = doc[ln]
                                name = ln
                                break
                        if ent: break

                if ent:
                    if ctx.has_flag("open"):
                        field = ctx.get_flag("open")
                        url = ent.get(field)
                        if url:
                            webbrowser.open(url)
                        else:
                            ctx.writeln("Field is not valid.")

                    elif ctx.has_flag("key"):
                        field = ctx.get_flag("key")
                        ctx.writeln(f"{field} = {ent[field]}")
                    else:
                        self.pretty_print_entity(ctx, name, ent, db)
                    return

                ctx.writeln("Could not find entry.")

            case "list" | "ls":
                if ln != "":
                    doc = ctx.get_data(ln, fmt='toml')
                    for ent in doc.keys():
                        body = doc[ent]
                        self.pretty_print_entity(ctx, ent, body, ln)
                else:
                    for filename in os.listdir(ctx.data_path()):
                        dbname = filename.split(".")[0]

                        if dbname in ctx.touch_config("codex.ignores", []):
                            continue

                        doc = ctx.get_data(dbname, fmt='toml')
                        if not doc.get("_aos_", {}).get("hidden from list", False):
                            for k, v in doc.items():
                                if k != "_aos_" and not v.get("hidden from list", False):
                                    if ctx.has_flag("compact") or ctx.has_flag("c"):
                                        t = v.get('text', '').strip()
                                        def comp(text):
                                            ln = text
                                            nl = False
                                            if "\n" in text: nl = True
                                            if len(ln) > 50: ln = ln[:50]+"..."
                                            if nl: ln = ln.split("\n")[0]+" ->"
                                            return ln

                                        ctx.writeln(f"[blue]{dbname}[/blue]:[blue]{k}[/blue]: {comp(t)}")
                                    else:
                                        self.pretty_print_entity(ctx, k, v, dbname)


        ctx.exit_code(0)
        return ctx

    def pretty_print_entity(self, ctx, ent, body, db):
        text = f"[red]{ent}[/red] in [red]{db}[/red]"
        if not body.get("compact"):
            for k, v in body.items():
                if type(v) == tomlkit.items.String:
                    if "\n" in v:
                        text += f"\n - [blue]{k}[/blue]:"
                        for ln in v.strip().split("\n"):
                            if ln.lower().startswith("x "):
                                text += f"\n  | [yellow strike]{ln[2:]}[/yellow strike]"
                            else:
                                text += f"\n  | [blue]{ln}[/blue]"
                    elif v.startswith("@ "):
                        d = " ".join(v.split(" ")[1:])
                        text += f"\n - [blue]{k}[/blue] = [blue]{d}[/blue] ([green]{ctx.utils.human_friendly_date(d)}[/green])"
                    else:
                        text += f"\n - [blue]{k}[/blue] = [blue]{v}[/blue]"

                elif type(v) == tomlkit.items.Array:
                    text += f"\n - [blue]{k}[/blue]\n"
                    for entry in v:
                        if entry.startswith("x "):
                            text += f"   + [yellow strike]{entry[2:]}[/yellow strike]\n"
                        else:
                            text += f"   + [blue]{entry}[/blue]\n"
                    text = text.strip()
                else:
                    text += f"\n - [blue]{k}[/blue] = [blue]{v}[/blue]"
        else:
            text = text + " ->"

        ctx.write_panel(text.strip())

    def pretty_print_entity_eno_depr(self, ctx, ent, db):
        text = f"[red]{ent.string_key()}[/red] in [red]{db}[/red]"
        if not ent.field("compact").optional_boolean_value():
            for elem in ent.elements():
                if elem.yields_field():
                    k = elem.to_field()
                    if "\n" in k.optional_string_value():
                        text += f"\n - [blue]{k.string_key()}[/blue]:"
                        for ln in k.optional_string_value().split("\n"):
                            if ln.lower().startswith("x "):
                                text += f"\n  | [yellow strike]{ln[2:]}[/yellow strike]"
                            else:
                                text += f"\n  | [blue]{ln}[/blue]"

                    elif k.optional_string_value().startswith("@ "):
                        d = " ".join(k.optional_string_value().split(" ")[1:])
                        text += f"\n - [blue]{k.string_key()}[/blue] = [blue]{d}[/blue] ([green]{ctx.utils.human_friendly_date(d)}[/green])"
                    else:
                        text += f"\n - [blue]{k.string_key()}[/blue] = [blue]{k.optional_string_value()}[/blue]"

                elif elem.yields_list():
                    k = elem.to_list()
                    text += f"\n - [blue]{k.string_key()}[/blue]\n"
                    for entry in k.required_string_values():
                        if entry.startswith("x "):
                            text += f"   + [yellow strike]{entry[2:]}[/yellow strike]\n"
                        else:
                            text += f"   + [blue]{entry}[/blue]\n"

        else:
            text = text + " ->"


        ctx.write_panel(text.strip())
