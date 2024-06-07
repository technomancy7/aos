import os, json
import webbrowser
import random

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
        Flags:
            --db:<database>
                Use a different database name, useful for grouping different entities together

        Commands:
            edit | write | e | w
            Opens document for the database in code editor

            search | s <<key>> = <<value>>
            Shows entries which contain a <<key>> and <<value>> match

            get [<<db>>].<<name>>
            Shows entry with matching <<name>>
                --open:<<field>> - Opens field in browser if it is a valid URL
                --rand:<<field>> - Choses random element from a comma-separated line

            list | ls (default)
            Shows all entries

            db <<name>>
            If no name given, lists all database names.
            Else changes active database.


        """

    def get_display_name(self, ctx, name, db = "addrbook"):
        doc = ctx.get_data_doc(db, override="codex") # override since this function may be called remotely

        for ent in doc.sections():
            if name.lower() == ent.string_key().lower():
                return ent.field("Display Name").optional_string_value() or "Default User"

    def __run__(self, ctx):
        cmd = ctx.get_string_ind(0)

        db = ctx.touch_config("codex.database", "addrbook")
        if ctx.has_flag("db"):
            db = ctx.get_flag("db")
            ctx.set_config("codex.database", db)
            ctx.writeln("Updated default database record: "+db)

        if cmd == "" or cmd == None: cmd = "list"

        match cmd:
            case "db":
                new = ctx.get_string()[len(cmd)+1:]
                if new:
                    ctx.set_config("codex.database", new)
                    ctx.writeln("Updated default database record: "+new)
                else:
                    ctx.writeln("Databases:")
                    for n in ctx.get_data_list():
                        if not n.endswith(".eno"): continue
                        ctx.writeln(f" [blue]{n.split('.')[0]}[/blue]")

            case "edit" | "write" | "e" | "w":
                new = ctx.get_string()[len(cmd)+1:]
                if new:
                    db = new
                ctx.writeln("Opening "+ctx.data_path()+db+".eno")
                ctx.edit_code(ctx.data_path()+db+".eno")

            case "search" | "s":
                doc = ctx.get_data_doc(db)
                searchstr = ctx.get_string()[len(cmd)+1:]
                k = searchstr.split("=")[0].strip()
                v = searchstr.split("=")[1].strip()

                for ent in doc.sections():
                    for elem in ent.elements():
                        field = elem.to_field()
                        if field.string_key().lower() == k.lower() and \
                        field.optional_string_value().lower() == v.lower():
                            self.pretty_print_entity(ctx, ent)

            case "get" | "g":
                name = ctx.get_string()[len(cmd)+1:]
                if "." in name:
                    db = name.split(".")[0]
                    name = name.split(".")[1]

                doc = ctx.get_data_doc(db)
                for ent in doc.sections():
                    if name.lower() == ent.string_key().lower():
                        if ctx.has_flag("open"):
                            field = ctx.get_flag("open")
                            try:
                                url = ent.field(field).required_url_value()
                                webbrowser.open(url)
                            except:
                                ctx.writeln("Field is not valid.")
                        elif ctx.has_flag("rand"):
                            field = ctx.get_flag("rand")
                            try:
                                v = ent.field(field).required_comma_separated_value()
                                ctx.writeln(random.choice(v))
                            except:
                                ctx.writeln("Field is not valid.")
                        else:
                            self.pretty_print_entity(ctx, ent)
                        return

                ctx.writeln("Could not find entry.")

            case "list" | "ls":
                new = ctx.get_string()[len(cmd)+1:]
                if new:
                    db = new
                doc = ctx.get_data_doc(db)

                for ent in doc.sections():
                    self.pretty_print_entity(ctx, ent)

        ctx.exit_code(0)
        return ctx

    def pretty_print_entity(self, ctx, ent):
        text = f"[red]{ent.string_key()}[/red]"

        for elem in ent.elements():
            if elem.yields_field():
                k = elem.to_field()
                if "\n" in k.optional_string_value():
                    text += f"\n - [blue]{k.string_key()}[/blue]:"
                    for ln in k.optional_string_value().split("\n"):
                         text += f"\n  | [blue]{ln}[/blue]"
                else:
                    text += f"\n - [blue]{k.string_key()}[/blue] = [blue]{k.optional_string_value()}[/blue]"

            elif elem.yields_list():
                k = elem.to_list()
                entries = "\n".join([f"   + [yellow]{entry}[/yellow]" for entry in k.required_string_values()])
                text += f"\n -- [blue]{k.string_key()}[/blue]\n{entries}"

            elif elem.yields_section():
                k = elem.to_section()

                text += f"\n\n [green]{k.string_key()}[/green]"
                for f in k.elements():
                    if f.yields_field():
                        k2 = f.to_field()
                        if "\n" in k2.optional_string_value():
                            text += f"\n - [blue]{k2.string_key()}[/blue]:"
                            for ln in k2.optional_string_value().split("\n"):
                                 text += f"\n  | [blue]{ln}[/blue]"
                        else:
                            text += f"\n - [blue]{k2.string_key()}[/blue] = [blue]{k2.optional_string_value()}[/blue]"

                    elif f.yields_list():
                        k2 = f.to_list()
                        entries = "\n".join([f"   + [yellow]{entry}[/yellow]" for entry in k2.required_string_values()])
                        text += f"\n - [blue]{k2.string_key()}[/blue]\n{entries}"

        ctx.write_panel(text)
