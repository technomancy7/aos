from pykeepass import PyKeePass
import pyperclip
import os, webbrowser
import pyotp

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "keyli",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            Commands:
                show

            Filters:
                title
                username
                password
                url
        """

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()
        db_path = ctx.touch_config("keyli.db", "Passwords.kdbx")
        db_pwd = ""

        if ctx.has_flag("pwd"):
            db_pwd = ctx.get_flag("pwd")

        if db_pwd == "" and os.getenv("KEYCLI_PWD"):
            db_pwd = os.getenv("KEYCLI_PWD")

        if db_pwd == "":
            db_pwd = ctx.touch_config("keyli.pwd", "")

        if not db_pwd:
            ctx.writeln("No database password given.")
        else:
            db = PyKeePass(db_path, password=db_pwd)

            def print_entry(e):
                show_pwd = ctx.has_flag("showpwd")
                ctx.write_panel(f"""{e.username} / {e.password if show_pwd else "****"}\n[green]URL[/green]: {e.url if e.url else "None"}\n[green]OPT[/green]: {pyotp.parse_uri(e.otp).now() if e.otp else "None"}""", title = e.title)

            def filter_entries():
                entries = []
                g = None
                if ctx.has_flag("group"):
                    g = db.find_groups(name=ctx.get_flag("group"), first=True)

                entries = db.find_entries(title=ctx.get_flag("title", None), username=ctx.get_flag("username", None), password=ctx.get_flag("password", None), url=ctx.get_flag("url", None), group=g)

                if len(entries) == 1:
                    return entries[0]

                if len(entries) == 0:
                    return None

                names = [f"{entry.title}/{entry.username}" for entry in entries]
                e = ctx.g.choose("Which entry?", *names)
                return entries[names.index(e)]

            match cmd:
                case "groups":
                    ctx.writeln(f"{[g.name for g in db.groups]}")

                case "copy":
                    e = filter_entries()

                    if e:
                        pyperclip.copy(e.password)
                        ctx.writeln(f"Password of {e.title}/{e.username} saved to clipboard.")

                case "copyotp":
                    e = filter_entries()

                    if e:
                        pyperclip.copy(pyotp.parse_uri(e.otp).now())

                case "showotp":
                    e = filter_entries()

                    if e:
                        ctx.writeln(pyotp.parse_uri(e.otp).now())

                case "show":
                    e = filter_entries()

                    if e:
                        print_entry(e)

                case "attach":
                    pass

                case "open":
                    e = filter_entries()
                    if e.url:
                        webbrowser.open(e.url)

                case "delete":
                    pass

                case "new":
                    pass

                case "newgroup":
                    pass



        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
