from multiprocessing import allow_connection_pickling
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import sys, os
HOME = os.path.expanduser("~")+"/"
ATHENAOS_PATH = HOME+".aos/"
sys.path.append(ATHENAOS_PATH+"lib/")
from objects import Context

class AosWin:
    def send_text(self, w):
        text = self.entry.get_text()
        print(text)
        self.entry.set_text("")
        self.add_log(text)
        self.context.update_from_line(text)
        self.context.execute()

        resp = self.context.response
        for log in resp["log"]:
            self.add_log(log.strip(), top=False)
    def add_log(self, line, top = False):
        self.log.set_editable(True)
        text = self.logbuffer.get_text(self.logbuffer.get_start_iter(), self.logbuffer.get_end_iter(), True)
        if top:
            text = line+"\n"+text
        else:
            text = text+"\n"+line
        self.logbuffer.set_text(text)
        self.log.set_editable(False)

    def __init__(self, app):
        self.context = Context()
        self.window = Gtk.ApplicationWindow(application=app)
        self.window.set_title("AthenaOS")
        self.window.set_default_size(600, 400)
        all_wdg = Gtk.Box()
        print(all_wdg.set_orientation(Gtk.Orientation.VERTICAL))
        box = Gtk.Box()
        
        box.set_hexpand(True)
        box.set_vexpand(False)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
            
        btn = Gtk.Button(label="Submit!")
        btn.connect('clicked', self.send_text)
        

        #logcont = Gtk.Box()
        self.log = Gtk.TextView()
        self.log.set_editable(False)
        self.logbuffer = self.log.get_buffer()
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_child(self.log)

        self.window.set_child(all_wdg)
        all_wdg.append(box)
        box.append(self.entry)
        box.append(btn)
        #logcont.append(self.log)
        all_wdg.append(scrolledwindow)

        self.window.present()


class AosWin2:
    def __init__(self, app):
        win = Gtk.ApplicationWindow(application=app)
        win.set_title("Log")
        box = Gtk.Box()
        win.set_child(box)
        self.entry = Gtk.Entry()
        box.append(self.entry)
            
        btn = Gtk.Button(label="Submit!")
        box.append(btn)
        win.present()

app = Gtk.Application(application_id='org.tcm.AthenaOS')
app.connect('activate', AosWin)
#app.connect('activate', AosWin2)
app.run(None)