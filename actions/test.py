from tools.converters import PhoneButtonConverter
from tools.virustotal import VirusTotal
import json

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "test",
            "author": "Kaiser",
            "version": "0.4",
            "features": [],
            "group": "system",
        }
    
    def __run__(self, ctx):
        #cmd, ln = ctx.cmdsplit()
        ln = ctx.get_string()
        #print(ln)
        #print(cmd, ",", line)
        #print(PhoneButtonConverter().convert(ln))
        #with rich.console.Console().pager():
            #ctx.writeln("Hmm")

        scanner = VirusTotal(ctx.touch_config("keys.virustotal"))
        #scanner.analysis(scanner.scan_file(ln))
        a = scanner.analysis(scanner.scan_url(ln))
        print(json.dumps(a, indent=4))
        
    def __help__(self, ctx):
        print("Helpless.")
        
    def __finish__(self, ctx):
        print("Test has finished.")