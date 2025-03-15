import os, importlib

class Action:
    @staticmethod
    def __action__():
        return {
        "name": "system",
        "author": "Kaiser",
        "version": "0.2",
        "features": [],
        "group": "system",
    }

    def __help__(self, ctx):
        return """
        System commands
        Generic utilities for AOS

        Commands:
            log.purge
                - Clears the log file.

            pipe.listen <pipename>
            pipe.send <pipename> <text>
        """

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()

        match cmd:
            case "list.get":
                print(ctx.get_textlist(ln))

            case "list.delete":
                print(ctx.delete_textlist(ln))
                
            case "list.remove":
                name = ln.split(" ")[0]
                v = " ".join(ln.split(" ")[1:])
                print(ctx.remove_textlist(name, v))

            case "list.append":
                name = ln.split(" ")[0]
                v = " ".join(ln.split(" ")[1:])
                print(ctx.append_textlist(name, v))

            case "log.purge":
                with open(ctx.aos_dir+"self.log", "w+") as f:
                    f.write("")

            case "pipe.listen":
                m = ctx.listen_for_pipe(ln, ctx.say)
                ctx.say(m)
            case "pipe.send":
                ctx.send_message_to_pipe(ln.split(" ")[0], " ".join(ln.split(" ")[1:]))

        return ctx
