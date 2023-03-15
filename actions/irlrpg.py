
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "irlrpg",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
        }

    def give_exp(self, num):
        to_next = self.ctx.touch_config("rpg.exp_to_next_level", 100)
        cur_exp = self.ctx.touch_config("rpg.exp", 0)
        lvl = self.ctx.touch_config("rpg.level", 1)

        if self.ctx.touch_config("rpg.show_exp", True):
            self.ctx.writeln(f"[blue] Gained {num} EXP.[/blue]")

        cur_exp = cur_exp + num

        if cur_exp > to_next:
            if self.ctx.touch_config("rpg.show_level", True):
                self.ctx.writeln(f"[green] Level up! ({lvl+1})[/green]")
            self.ctx.set_config("rpg.level", lvl + 1, save = False)
            self.ctx.set_config("rpg.exp_to_next_level", int(to_next*1.2), save = False)
            cur_exp -= to_next

        self.ctx.set_config("rpg.exp", int(cur_exp))
        return cur_exp

    def __help__(self, ctx):
        return """
            Default help.
        """

    def __run__(self, ctx): 
        # Main functionality here.
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

