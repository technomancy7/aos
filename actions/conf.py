from ast import parse
import os
from tools.datascript import *
import tomlkit
import tomlkit.items

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "conf",
            "author": "Kaiser",
            "version": "1.0",
            "features": [],
            "group": "utility",
    }

    def __help__(self, ctx):
        return """
        Commands:
            set <<parent.>key> <value>
            get <<parent.>key>
            append <<parent.>key> <value>
            unappend <<parent.>key> <value>
            unset <<parent.>key>
            list

        """

    def parse_val(self, line):
        if line == "true": return True
        if line == "false": return False
        try:
            return eval(line)
        except:
            return line


    def __run__(self,ctx):
        cmd = ""
        line = []
        if ctx.get_string() == "":
            cmd = "list"

        else:
            cmd = ctx.get_string_list()[0]
            line = ctx.get_string_list()[1:]

        ctx.update_response(operator = cmd)
        conf = ctx.config
        if cmd == "set":
            key = line[0]
            val = self.parse_val(" ".join(line[1:]))

            ctx.set_config(key, val)
            ctx.writeln(f"[yellow]{key}[/yellow] = [green]{val}[/green] ({type(val)})")
            ctx.update_response(key = key, value = val)
            ctx.save_config()

        elif cmd == "unset":
            key = line[0]
            val = self.parse_val(" ".join(line[1:]))

            ctx.unset_config(key)
            ctx.writeln(f"[yellow]{key}[/yellow] = [green]None[/green] (None)")
            ctx.update_response(key = key)
            ctx.save_config()

        elif cmd == "unappend":
            key = line[0]
            line = self.parse_val(" ".join(line[1:]))
            ls = ctx.touch_config(key, None)
            if type(ls) == tomlkit.items.Array:
                ls.remove(line)
                ctx.set_config(key, ls)
                ctx.writeln(f"[yellow]{key}[/yellow] = [green]{ls}[/green] ({type(ls)})")
                ctx.update_response(key = key, value = ls)
            else:
                return ctx.writeln(f"Invalid type for {line}. Expected {type([])}, got {type(ls)}.")

        elif cmd == "append":
            key = line[0]
            line = self.parse_val(" ".join(line[1:]))
            ls = ctx.touch_config(key, None)
            #print(key, ls)
            if type(ls) == tomlkit.items.Array:
                ls.append(line)
                ctx.set_config(key, ls)
                ctx.writeln(f"[yellow]{key}[/yellow] = [green]{ls}[/green] ({type(ls)})")
                ctx.update_response(operator = "append", key = key, value = ls)
            elif type(ls) == tomlkit.items.String:
                ls += line
                ctx.set_config(key, ls)
                ctx.writeln(f"[yellow]{key}[/yellow] = [green]{ls}[/green] ({type(ls)})")
                ctx.update_response(operator = "append", key = key, value = ls)
            else:
                return ctx.writeln(f"Invalid type for {line}. Expected {type([])} or {type('')}, got {type(ls)}.")

        elif cmd == "get":
            key = " ".join(line)
            val = ctx.touch_config(key, "", ignore = True)
            ctx.update_response(operator = "get", key = key, value = val)
            t = type(val)
            #print(t)
            if t != bool and t != tomlkit.items.Table: t = type(t.unwrap(t))
            ctx.writeln(f"[yellow]{key}[/yellow] = [green]{val}[/green] ({t.__name__})")

        elif cmd == "edit":
            ctx.edit_file(ctx.aos_dir+"config.json")

        elif cmd == "list":
            compacts = conf.get('compact', [])
            ind = False

            for k, v in conf.items():
                if type(v) == tomlkit.items.Table:
                    ind = True
                    ctx.writeln()

                    ctx.writeln(f"[blue]{k}[/blue]: {v.trivia.comment}")

                    if k not in compacts:
                        for sk, sv in v.items():
                            if type(sv) == bool:
                                b = v.value.item(sk)
                                ctx.writeln(f"- [yellow]{sk}[/yellow] = [green]{sv}[/green] ({type(sv).__name__}) {b.trivia.comment}")
                            else:
                                ctx.writeln(f"- [yellow]{sk}[/yellow] = [green]{sv}[/green] ({type(sv.unwrap()).__name__}) {sv.trivia.comment}")
                    else:
                        ctx.writeln(f"{len(list(v.items()))} items")

                else:
                    if ind:
                        ctx.writeln()
                        ind = False

                    if type(v) == bool:
                        ctx.writeln(f"[yellow]{k}[/yellow] = {v} ({type(v).__name__}) {conf.item(k).trivia.comment}")
                    else:
                        ctx.writeln(f"[yellow]{k}[/yellow] = {v} ({type(v.unwrap()).__name__}) {v.trivia.comment}")

            ctx.writeln()
        else:
            return ctx.writeln("What?")
        return ctx
