
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "irlrpg",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def give_exp(self, exp):
        next_level = int(self.ctx.touch_config("irlrpg.level", 1) * 100 * 1.1)

        cur = self.ctx.touch_config("irlrpg.current_exp", 0)
        cur += int(exp)
        self.ctx.writeln(f"Gained EXP: +{exp} {cur}/{next_level}")


        if cur > next_level:
            cur = cur - next_level
            self.ctx.set_config("irlrpg.level", self.ctx.touch_config("irlrpg.level", 1) + 1)
            lvl = self.ctx.touch_config("irlrpg.level", 1)
            next_level = int(lvl * 100 * 1.1)
            self.ctx.writeln(f"Level up! Now {lvl}. ({cur}/{next_level})")

        self.ctx.set_config("irlrpg.current_exp", cur)

    def __help__(self, ctx):
        return """
        """

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()
        # Main functionality here.
        match cmd:
            case "status":
                lvl = self.ctx.touch_config("irlrpg.level", 1)
                next_level = int(lvl * 100 * 1.1)
                cur = self.ctx.touch_config("irlrpg.current_exp", 0)
                ctx.writeln(f"Level: {lvl}, {cur}/{next_level} to next level.")
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
