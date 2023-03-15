import rich

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
        cmd, ln = ctx.cmdsplit()
        print(cmd)
        print(ln)
        #print(cmd, ",", line)
        print(ctx.get_flag("test"))
        #with rich.console.Console().pager():
            #ctx.writeln("Hmm")
            
    def __help__(self, ctx):
        print("Helpless.")
        
    def __finish__(self, ctx):
        print("Test has finished.")