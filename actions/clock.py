
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "clock",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            Default help.
        """
        
    def add_timer(self, name, s):
        if not self.data.get("timers"):
            self.data["timers"] = {}
        
        self.data["timers"][name] = {"time_left": s, "time_start": s, "state": "active"}
        self.ctx.save_data(self.data)
        
    def edit_timer(self, name, key, val):
        if self.data.get("timers") and self.data["timers"].get(name):
            self.data["timers"][name][key] = val
            
            self.ctx.save_data(self.data)
            
    def delete_timer(self, name):
        if self.data.get("timers") and self.data["timers"].get(name):
            del self.data["timers"][name]
            
            self.ctx.save_data(self.data)
            
    def __run__(self, ctx): 
        cmd, ln = ctx.cmdsplit()
        self.data = ctx.get_data()
        self.ctx = ctx
        match cmd:
            case "timer" | "t":
                print("Timer")
            
            case "worldclock" | "wc":
                print("World")
                
            case "alarm" | "a":
                print("alarm")
            
            case other:
                print("Unknown")
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

