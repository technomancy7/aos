import os
from rivescript import RiveScript
import rivescript
import rich

class AOSSessionManager(rivescript.sessions.SessionManager):
    def __init__(self, aos_ctx):
        self.aos = aos_ctx
        self.rs = None
        self.local_file = f"{self.aos.aos_dir}brain/local.ai"

    def add_code(self, block):
        print("try stream [", block, "]")
        self.rs.stream(block)
        with open(self.local_file, "a+") as f:
            f.write(f"\n\n{block}")

    def remove_code(self, block):
        text = ""
        with open(self.local_file, "r") as f:
            text = f.read()
        text = text.replace(block, "")
        text = text.strip()
        with open(self.local_file, "w") as f:
            f.write(text)

    def tidy_code(self):
        text = ""
        with open(self.local_file, "r") as f:
            text = f.read()

        while "\n\n" in text: text = text.replace("\n\n", "\n")
        text = text.strip()
        with open(self.local_file, "w") as f:
            f.write(text)

    def get_all(self):
        return self.aos.touch_config("talk_sessions")

    def freeze(self, username):
        data = self.aos.touch_config(f"talk_sessions.{username}", {})
        df = self.aos.get_data()
        df[username] = data
        self.aos.save_data(df)

    def thaw(self, username, action="thaw"):
        userdata = self.aos.touch_config(f"talk_sessions.{username}", {})
        df = self.aos.get_data()
        udf = df.get(username, {})

        if action == "thaw" or action == "keep":
            for k, v in udf.items():
                userdata[k] = v

            self.aos.set_config(f"talk_sessions.{username}", userdata)

        if action == "thaw" or action == "discard":
            del df[username]
            self.aos.save_data(df)

    def get(self, username, var, default = "undefined"):
        data = self.aos.touch_config(f"talk_sessions.{username}", {})
        return data.get(var, None)

    def set(self, username, dic):
        data = self.aos.touch_config(f"talk_sessions.{username}", {})
        for k, v in dic.items():
            if v == None:
                del data[k]
            else:
                data[k] = v
        self.aos.set_config(f"talk_sessions.{username}", data)

class Action:
    @staticmethod
    def __action__():
        return {
        "name": "talk",
        "author": "Kaiser",
        "version": "0.4",
        "features": [],
        "group": "system",
    }

    def __help__(self, ctx):
        pass

    def __run__(self, ctx):
        ctx.set_config("talk.active", True)
        braindir = ctx.touch_config("talk.brain", ctx.aos_dir+"brain/")

        username = ctx.username()
        rs = RiveScript(session_manager=AOSSessionManager(ctx))
        rs._session.rs = rs
        rs.load_directory(braindir, ext=['ai', 'rive'])
        rs.sort_replies()
        line = ctx.get_string()

        def execute(ln):
            firstpart = ln.split(" ")[0]
            rest = " ".join(ln.split(" ")[1:])
            output = ""
            match firstpart:
                case "/" | "/h" | "/help" | "/cmd":
                    ctx.writeln(f"AI PARSER HELP")
                    ctx.writeln("/quit, /edit <rs file name>, /aos <aos command>, /console <terminal command>")
                    ctx.writeln("/loop <counter> <text>, /repeat <history index>, /remind <code>, /forget <code>")
                    ctx.writeln("/thaw, /freeze, /set, /get /showall")
                case "/quit" | "/q":
                    exit()
                case "/edit":
                    ctx.edit_code(ctx.aos_dir+"/brain/"+rest)
                case "/aos":
                    ctx.quick_run(rest)
                case "/console":
                    os.system(rest)
                case "/cycle" | "/loop":
                    c = rest.split(" ")[0]
                    rest = " ".join(rest.split(" ")[1:])
                    if c.isdigit():
                        reply = ""
                        for i in range(0, int(c)):
                            reply += rs.reply(username, rest)+" "
                        return reply
                case "/repeat" | "/redo" | "/again":
                    inx = 0
                    if rest.isdigit():
                        inx = int(rest)
                    rln = ctx.touch_config(f"talk_sessions.{username}")["__history__"]["input"][0]
                    reply = rs.reply(username, rln)
                    return reply
                case "/remind":
                    rs._session.add_code(rest.replace("->", "\n"))
                case "/forget":
                    rs._session.remove_code(rest.replace("->", "\n"))
                case "/freeze":
                    rs._session.freeze(username)
                case "/thaw":
                    rs._session.thaw(username)
                case "/set":
                    key = rest.split(":")[0]
                    val = ":".join(rest.split(":")[1:]).strip()
                    rs._session.set(username, {key: val})
                case "/get":
                    ctx.writeln(rs._session.get(username, rest))
                case "/showall":
                    ctx.writeln(rs._session.get_all())
                case other:
                    reply = rs.reply(username, ln)
                    return reply
            return output

        if line == "":
            while True:
                line = ctx.getln(f"[blue]({username})[/blue]> ")
                res = ""
                if ", then " in line:
                    for subln in line.split(", then"):
                        res += execute(subln)+" "
                else:
                    res += execute(line)+" "

                if res.strip(): ctx.say(res.strip())
        else:
            res = ""
            if ", then " in line:
                for subln in line.split(", then"):
                    ctx.writeln(f"[blue]({username})[/blue]> {subln}")
                    res += execute(subln)+" "
            else:
                ctx.writeln(f"[blue]({username})[/blue]> {line}")
                res += execute(line)+" "
            if res.strip(): ctx.say(res.strip())
        return ctx

    def __finish__(self, ctx):
        ctx.set_config("talk.active", False)
