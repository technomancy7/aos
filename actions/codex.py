import os, json

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

            get <<name>>
            Shows entry with matching <<name>>

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
            print("Updated default database record: "+db)

        data = ctx.get_data(db)

        if cmd == "" or cmd == None: cmd = "list"
        ctx.writeln(f" --- Currently active: [blue]{db}[/blue] ---")
        ctx.writeln("")
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
                doc = ctx.get_data_doc(db)
                name = ctx.get_string()[len(cmd)+1:]
                for ent in doc.sections():
                    if name.lower() == ent.string_key().lower():
                        self.pretty_print_entity(ctx, ent)

            case "list" | "ls":
                doc = ctx.get_data_doc(db)

                for ent in doc.sections():
                    self.pretty_print_entity(ctx, ent)

        ctx.exit_code(0)
        return ctx

    def pretty_print_entity(self, ctx, ent):
        ctx.writeln(f"# [blue]{ent.string_key()}[/blue]")
        for elem in ent.elements():
            k = elem.to_field()
            ctx.writeln(f" - [blue]{k.string_key()}[/blue] = [blue]{k.optional_string_value()}[/blue]")
        ctx.writeln("")
