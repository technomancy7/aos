from atproto import Client
import textwrap

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "bsky",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            Interface with the bsky AT protocol.
        """

    def __run__(self, ctx):
        host = ctx.get_flag("host") or ctx.touch_config("bsky.host", "https://bsky.social")
        user = ctx.get_flag("user") or ctx.touch_config("bsky.user", "")
        pwd = ctx.get_flag("pwd") or ctx.touch_config("bsky.pwd", "")
        cmd, ln = ctx.cmdsplit()

        if user == "" and pwd == "":
            ctx.writeln("Login details missing.")
            return

        match cmd:
            case "post" | "p" | "send" | "s":
                if ln == "":
                    ctx.writeln("Nothing to send.")
                    return

                client = Client(base_url=host)
                client.login(user, pwd)
                post = client.send_post(ln)
                ctx.writeln(post.uri)
                return ctx

            case "profile" | "view" | "user":
                client = Client(base_url=host)
                client.login(user, pwd)
                data = client.get_profile(actor=ln)
                #print(data)
                did = data.did
                display_name = data.display_name
                ctx.write_panel(textwrap.dedent(f"""
                {display_name} ({did})
                {data.handle} ({data.posts_count} posts)
                {data.labels}
                {data.description}
                """))
            case default:
                ctx.writeln("?")

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
