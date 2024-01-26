from pykeepass import PyKeePass

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "pwd",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            Default help.
        """

    def __gui__(self, sender, app, data):
        label = data['label']
        context = data['context']
        pos = context.touch_config(f"gui.{label}_pos", [0, 19])
        height = context.touch_config(f"gui.{label}_height", 0)
        width = context.touch_config(f"gui.{label}_width", 0)

        if data["init"](label):
            dpg = data['dpg']
            with dpg.window(label=label, tag=label, pos = pos, width = width, height = height, on_close = lambda: data["close"](label)):
                dpg.add_button(callback=None, label=label)

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()
        self.db_path = ctx.touch_config("pwd.db", "Passwords.kdbx")
        self.password = ctx.touch_config("pwd.password", "")
        self.db = PyKeePass(self.db_path, password=self.password)

        match cmd:
            case "l" | "ls":
                for entry in self.db.entries:
                    ctx.writeln(f"{entry.title}")
                    ctx.writeln(f"{entry.username} - {entry.password}")

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

