
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "memo",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            A simple memo system, store and recall text.

            add <text>
                Appends text to current memo.

            edit
                Opens memo in text editor.

            print
                Prints current memo.

            set <text>
                Overwrites current memo.

            store <optional name>
                Saves current memo to the database storage under the defined name.
                Shows current store if no name given.

            recall <name>
                Sends text from database storage label to current memo.
        """

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()

        match cmd:
            case "store":
                d = ctx.get_data()
                if not ln:
                    for k, v in d.items():
                        ctx.write_panel(f"{v}", title = k)
                    return

                txt = ctx.touch_config("memo.text", "")

                d[ln] = txt
                ctx.save_data(d)

            case "recall":
                if not ln:
                    return self.writeln("A name is needed.")

                d = ctx.get_data()
                if d.get(ln):
                    ctx.set_config("memo.text", d[ln])

            case "clear" | "reset":
                ctx.set_config("memo.text", "")

            case "a" | "add" | "append":
                if not ln:
                    return self.writeln("Missing text.")

                txt = ctx.touch_config("memo.text", "")
                txt += f"\n{ln}"
                ctx.set_config("memo.text", txt)

            case "edit" | "e":
                txt = ctx.touch_config("memo.text", "")
                txt = ctx.open_text_editor(txt)
                ctx.set_config("memo.text", txt)

            case "get" | "print" | "g" | "p":
                ctx.writeln(ctx.touch_config("memo.text", ""))

            case "set" | "new" | "n":
                if not ln:
                    return self.writeln("Missing text.")
                ctx.set_config("memo.text", ln)

            case _:
                ctx.writeln(ctx.touch_config("memo.text", ""))

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
