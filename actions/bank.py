
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "bank",
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

    def add_transaction(self, account, amt, *, message="", data = None):
        d = data or self.ctx.get_data()
        if d.get("accounts", None) == None:
            d["accounts"] = {}

        if d["accounts"].get(account, None) == None:
            self.ctx.writeln("Account not found.")
            return None

        d["accounts"][account]["history"].append({"amt": amt, "message": message})

        d["accounts"][account]["current"] += amt
        self.ctx.save_data(d)
        return d["accounts"][account]

    def print_account(self, db, accname):
        acc = db["accounts"].get(accname)

        if acc:
            self.ctx.write_panel(f"Total: {db['currency']}{acc['current']}")
    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()

        match cmd:
            case "add":
                d = ctx.get_data()
                account = ctx.g.choose("Select account: ", *d["accounts"].keys())
                msg = ctx.g.get_input("Add an optional message:")
                amt = ctx.g.get_input("Input transaction amount:")
                result = self.add_transaction(account, float(amt), message=msg, data=d)
                self.print_account(d, account)

            case "check":
                d = ctx.get_data()
                account = ctx.g.choose("Select account: ", *d["accounts"].keys())
                self.print_account(d, account)

            case "delete":
                d = ctx.get_data()
                account = ctx.g.choose("Select account: ", *d["accounts"].keys())
                del d["accounts"][account]
                ctx.save_data(d)
                
            case "create":
                d = ctx.get_data()
                if d.get("accounts", None) == None:
                    d["accounts"] = {}

                if d["accounts"].get(ln, None) == None:
                    name = ctx.g.get_input("Choose a name:")
                    d["accounts"][name] = {"current": 0.0, "history": []}
                    ctx.save_data(d)
                    ctx.writeln("Added.")

            case "purge":
                ctx.save_data({})

            case "setup":
                d = ctx.get_data()

                currency = ctx.g.get_input(prompt="Input currency symbol")
                d["currency"] = currency

                if d.get("accounts", None)  == None or ctx.g.confirm("Delete all accounts?"):
                    d["accounts"] = {
                        "default": {"current": 0.0, "history": []}
                    }
                else:
                    ctx.writeln("No change made.")

                ctx.save_data(d)
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
