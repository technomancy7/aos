from ast import parse
import os
from tools.datascript import *

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
            if type(ls) == list:
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
            if type(ls) == list:
                ls.append(line)
                ctx.set_config(key, ls)
                ctx.writeln(f"[yellow]{key}[/yellow] = [green]{ls}[/green] ({type(ls)})")
                ctx.update_response(operator = "append", key = key, value = ls)
            elif type(ls) == str:
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
            ctx.writeln(f"[yellow]{key}[/yellow] = [green]{val}[/green] ({type(val)})")

        elif cmd == "list":
            #dc = Datascript().parse_file(ctx.aos_dir+"definitions.dcs")["variables"]
            dc = ctx.get_doc("definitions")
            #return print(dc.field("core.nae").optional_string_value())
            compacts = dc.list('compact').required_string_values()

            ind = False
            for k, v in conf.items():
                desc = ""
                if dc.field("root").optional_string_value():
                    desc = f" // {dc.field('root').optional_string_value()}"

                if type(v) == dict:
                    ind = True

                    ctx.writeln()
                    descmain = ""
                    if dc.field(k).optional_string_value():
                        descmain = f" // {dc.field(k).optional_string_value()}"
                    ctx.writeln(f"[blue]{k}[/blue]:{descmain}")

                    if k not in compacts:
                        for sk, sv in v.items():
                            desc2 = ""
                            if dc.field(k+"."+sk).optional_string_value():
                                desc2 = f" // {dc.field(k+'.'+sk).optional_string_value()}"
                            ctx.writeln(f"- [yellow]{sk}[/yellow] = [green]{sv}[/green] ({type(sv)}){desc2}")
                    else:
                        ctx.writeln(f"{len(list(v.items()))} items")

                elif type(v) == list:
                    ind = True
                    ctx.writeln()
                    ctx.writeln(f"[blue]{k}[/blue]:{desc}")
                    for item in v:
                        ctx.writeln(f"* [yellow]{item}[/yellow] ({type(item)})")

                else:
                    if ind:
                        ctx.writeln()
                        ind = False
                    desc2 = ""
                    if dc.field(k).optional_string_value():
                        desc2 = f" // {dc.field(k).optional_string_value()}"
                    ctx.writeln(f"[yellow]{k}[/yellow] = {v} ({type(v)}){desc2}")
        else:
            return ctx.writeln("What?")
        return ctx
