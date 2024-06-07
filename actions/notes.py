import os
from textwrap import dedent

class Action:
    @staticmethod
    def __action__():
        return {
        "name": "notes",
        "author": "Kaiser",
        "version": "1.0b",
        "features": [],
        "group": "utility",
    }

    def __help__(self, ctx):
        return dedent("""
        Commands:
            edit
                Opens note file in code editor.

            ls
                Lists notes.
                --s:<section> - only shows notes in section
                --d - only show notes not marked done

        Note format:
            # note group
            ## note title
            text: main body
            -- text
            multiline text
            goes here
            -- text
            done: yes // set if note considered done
            hidden: yes // set to hide from list
            list:
            - []Do a thing.
            - [x]Do other thing. //optional syntax to mark as done
            tags:
            - coding
        """)

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()
        hd = ctx.has_flag("d")
        tags = ctx.get_flag("ts").split(",") or []
        tag = ctx.get_flag("t") or ""


        if cmd == "" or cmd == None: cmd = "list"

        match cmd:
            case "edit" | "write":
                ctx.edit_code(ctx.data_path()+"data.eno")

            case "show" | "s" | "get" | "g":
                d = ctx.get_data_doc()
                for sect in d.sections():
                    #if fsect and sect.string_key() != fsect: continue

                    for note in sect.sections():
                        #print(ln, note.string_key())
                        if ln == note.string_key() or ln == note.field("key").optional_string_value():
                            t = [f"[blue]#[/blue][green]{tag}[/green]" for tag in note.list('tags').optional_string_values()]
                            if len(t) == 0: t = ""
                            else: t = " ".join(t)
                            text = f"< [yellow]{note.string_key()}[/yellow] in [red]{sect.string_key()}[/red] > {t}"
                            text = text + f'\n[white]{note.field("text").optional_string_value()}[/white]'

                            ls = note.list("list").optional_string_values()
                            if len(ls) > 0:
                                for en in ls:
                                    if en.startswith("[]"): en = en.replace("[]", "")
                                    if en.startswith("[x]"):
                                        en = f"[strike]{en}[/strike]"

                                    text = text + "\n :right_arrow: " + en
                            if note.field("done").optional_boolean_value():
                                text = text + "\n[red](Note is marked done.)[/blue]"
                            ctx.write_panel(text)

            case "list" | "ls" | "l":
                fsect = ctx.get_flag("s") or ln or ""
                d = ctx.get_data_doc()
                for sect in d.sections():
                    if fsect and sect.string_key() != fsect: continue

                    for note in sect.sections():
                        if not note.field("hidden").optional_boolean_value():
                            if hd and note.field("done").optional_boolean_value():
                                continue

                            notekey = note.field("key").optional_string_value()
                            if notekey: notekey = f"[yellow]{notekey}[/yellow] :: "
                            else: notekey = ""
                            t = [f"[blue]#[/blue][green]{tag}[/green]" for tag in note.list('tags').optional_string_values()]
                            if len(t) == 0: t = ""
                            else: t = " ".join(t)

                            dones = ""
                            if note.field("done").optional_boolean_value():
                                dones = " strike"
                            text = f"< {notekey}[yellow{dones}]{note.string_key()}[/yellow{dones}] in [red]{sect.string_key()}[/red] > {t}"

                            if not note.field("compact").optional_boolean_value():
                                #continue
                                if note.field("text").optional_string_value():
                                    text = text + f'\n[white{dones}]{note.field("text").optional_string_value()}[/white{dones}]'
                            else:
                                text = text + f'\n[white{dones}](Text: {len(note.field("text").optional_string_value())} characters...)[/white{dones}]'

                            ls = note.list("list").optional_string_values()
                            if len(ls) > 0:
                                for en in ls:
                                    if en.startswith("[]"): en = en.replace("[]", "")
                                    if en.startswith("[x]"):
                                        en = f"[strike]{en}[/strike]"

                                    text = text + "\n :right_arrow: " + en

                            ctx.write_panel(text)

        return ctx
