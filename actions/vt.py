from tools.virustotal import VirusTotal
import json

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "vt",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            analysis <id>
            search <query>
            file <filepath>
            url <url>

            Flags:  
                -f - Show full output
        """

    def print_analysis(self, ctx, data, full = False):
        a = data['data']['attributes']
        ctx.writeln(f"Harmless: {a['stats']['harmless']}")
        ctx.writeln(f"Malicious: {a['stats']['malicious']}")
        ctx.writeln(f"Suspicious: {a['stats']['suspicious']}")
        ctx.writeln(f"Undetected: {a['stats']['undetected']}")
        ctx.writeln(f"Timeouts: {a['stats']['timeout']}")

        if full:
            output = {}
            for k, v in a['results'].items():
                if output.get(v['category'], None) == None:
                    output[v['category']] = []

                output[v['category']].append(v)
                #ctx.writeln(f"{k} {v['category']} ({v['result']})")
            
            for k, v in output.items():
                ctx.writeln(f"== {k} ==")
                #text = 
                #or item in v:
                ctx.writeln(" | ".join([f"[red]{item['engine_name']}[/red]: {item['result']}" for item in v]))

    def __run__(self, ctx): 
        # Main functionality here.
        cmd, ln = ctx.cmdsplit()
        full_analysis = ctx.has_flag("f")
        scanner = VirusTotal(ctx.touch_config("keys.virustotal"))
        match cmd:
            case "analysis":
                a = scanner.analysis(ln)

                self.print_analysis(ctx, a, full_analysis)
            case "search":
                a = scanner.search(ln)
                #print(json.dumps(a, indent=4))
                if len(a) > 0:
                    for item in a:
                        attribs = item['attributes']
                        ctx.writeln(f"{attribs['votes']}")
                        ctx.writeln(attribs['text'])
                        ctx.writeln("----")
            case "file":
                vid = scanner.scan_file(ln)
                ctx.writeln(f"Scan ID: {vid}")
                a = scanner.analysis(vid)
                #print(json.dumps(a, indent=4))
                self.print_analysis(ctx, a, full_analysis)

            case "url":
                vid = scanner.scan_url(ln)
                ctx.writeln(f"Scan ID: {vid}")
                a = scanner.analysis(vid)
                #print(json.dumps(a, indent=4))
                self.print_analysis(ctx, a, full_analysis)
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

