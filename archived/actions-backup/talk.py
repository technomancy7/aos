import os
from rivescript import RiveScript
import rivescript
def action_data():
    return {
    "name": "talk",
    "author": "Kaiser",
    "version": "0.4",
    "features": [],
    "group": "system",
}

def on_help(ctx):
    pass

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

def on_load(ctx): 
    ctx.set_config("talk.active", True)
    braindir = ctx.touch_config("talk.brain", ctx.aos_dir+"brain/")
    #print("Loading", braindir)
    data = ctx.get_data()
    username = ctx.username()
    rs = RiveScript(session_manager=AOSSessionManager(ctx))
    rs._session.rs = rs
    rs.load_directory(braindir, ext=['ai'])
    rs.sort_replies()
    line = ctx.get_string()

    def execute(ln):
        print("INPUT", ln)
        firstpart = ln.split(" ")[0]
        rest = " ".join(ln.split(" ")[1:])

        match firstpart:
            case "/quit":
                exit()
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
                ctx.say(reply)

    if line == "":
        while True:
            line = input(f"({username})> ")
            execute(line)
    else:
        execute(line)

    return ctx

def on_exit(ctx):
    ctx.set_config("talk.active", False)