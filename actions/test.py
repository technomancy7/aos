
class Action:
    def __action_data__(self):
        return {
            "name": "test",
            "author": "Kaiser",
            "version": "0.4",
            "features": [],
            "group": "system",
        }
    
    def __run__(self, ctx):
        print("Test action has run.")

    def __help__(self, ctx):
        print("Helpless.")
        
    def __finish__(self, ctx):
        print("Test has finished.")