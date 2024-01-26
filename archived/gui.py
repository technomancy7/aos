from tkinter import *
from tkinter.ttk import *
import os, sys

HOME = os.path.expanduser("~")+"/"
ATHENAOS_PATH = HOME+".aos/"
sys.path.append(ATHENAOS_PATH+"lib/")

from objects import Context


class AOSMainWin:
    def __init__(self, master):
        self.context = Context()
        self.context.writeln = self.log
        self.master = master
        self.master.title("Athena")

        self.frame = Frame(self.master)
        self.frame.pack(expand = True, fill = BOTH)

        self.text = Entry(self.frame, width = 70)
        self.text.pack(expand = True, fill = BOTH, side=LEFT)
        
        self.text.bind("<Return>", lambda _: self.send_command())
        self.text.bind('<Tab>', lambda _: self.proc_tab())        
        self.master.bind("<Control-c>", lambda _: self.list_acts())

        self.text.focus_set()
        
        self.sub = {}
        
    def has_window(self, name):
        return self.sub.get(name) != None
    
    def new_window(self, name):
        self.sub[name] = {"window": Tk()}
        self.sub[name]["frame"] = Frame(self.sub[name]["window"])
        self.sub[name]["frame"].pack(expand = True, fill = BOTH)
        return self.sub[name]
                        
    def get_window(self, name):
        return self.sub[name]

    def destroy_window(self, name):
        r = self.get_window(name)
        
        widgets = r.winfo_children()
        for widget in widgets:
            widget.destroy()
        
        r.destroy()
        del self.sub[name]
                    
    def log(self, *line, **args):
        if not self.has_window("log"):
            lw = self.new_window("log")
            lw["text"] = Text(lw["frame"], undo = True, height = 20, width = 70)
            lw["text"].pack(expand = True, fill = BOTH)
        else:
            lw = self.get_window("log")
            
        text = " ".join(line)
        lw["text"].insert("end", text+"\n")
        
    def list_acts(self):
        lw = self.branch("actlist")
        lw.title("Actions")
        
    def proc_tab(self):
        print("Tab")
        
    def send_command(self):
        cmd = self.text.get()
        self.log(cmd)
        self.text.focus_set()
        #c = self.context.quick_run(cmd)
        
        
root = Tk()
window = AOSMainWin(root)
root.mainloop()
