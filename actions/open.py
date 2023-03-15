import re, os, webbrowser

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "open",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
        }

    def __help__(self, ctx):
        return """
            Default help.
        """
    
    def check_url_or_path(self, string):
        url_pattern = r'^(?:http(s)?://)?[\w\-]+(\.[\w\-]+)+[/#?]?.*$'
        path_pattern_win = r'^[\w\-. ]+(\/[\w\-. ]+)*\/?$'
        path_pattern_linux = r'^\/(?:[\w\-. ]+\/)*[\w\-. ]+$'

        if re.match(url_pattern, string) and not os.path.isfile(string):
            return 'url'
        elif re.match(path_pattern_linux, string) and os.path.isdir((string)):
            return 'dir'
        elif re.match(path_pattern_linux, string) and os.path.isdir((string)):
            return 'file'
        else:
            if os.path.isdir(string):
                return "dir"
            if os.path.isfile(string):
                return "file"
            return 'unknown'

    def __run__(self, ctx): 
        # Main functionality here.
        fpath = ctx.get_string()
        r = self.check_url_or_path(fpath)
        print(r)
        match r:
            case "file":
                os.system(f"open {fpath}")
            
            case "dir":
                pass

            case "url":
                webbrowser.open(fpath)

            case _:
                ctx.say("Could not interpret input.")
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

