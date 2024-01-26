import sys, os, importlib, random
import io
import textwrap
import contextlib, traceback
from contextlib import redirect_stdout

HOME = os.path.expanduser("~")+"/"
ATHENAOS_PATH = HOME+".aos/"
sys.path.append(ATHENAOS_PATH+"lib/")
from objects import Context
import dearpygui.dearpygui as dpg
#import dearpygui_ext.themes as themes

keys = {key: getattr(dpg, f"mvKey_{key.upper()}") for key in [
    *"ABCDEFGHIJKLMNOPQRSTUVWXYZ", 
    *"ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower(),
    *[str(i) for i in range(1, 10)], 
    *[f"F{i}" for i in range(1, 13)],
    *[f"f{i}" for i in range(1, 13)]
    ]}
context = Context(base_dir = ATHENAOS_PATH)
context.load_config()
context.plaintext_output = context.touch_config("plaintext", False)

win_width = context.touch_config("gui.width", 1024)
win_height = context.touch_config("gui.height", 600)
autostart = context.touch_config("gui.autostart", [])
last_session = context.touch_config("gui.last_session", [])
background = context.touch_config("gui.background", [50, 50, 50])
disabled = context.touch_config("system.disabled", [])
WINDOWS = []
ACTIONS = []
EXTENSIONS = []

session_persist = context.touch_config("gui.persist", False)
internal_apps = {
    "input": {
        "open": False
    },
    "log": {
        "open": False,
        "buffer": ""
    },
    "textedit": {
        "open": [],
        "_editors": 0
    },
    "imageview": {
        "open": [],
        "_views": 0
    }
}
log_buffer = ""
window_theme = None
aos_popup_data = {
    "confirmation": False
}

def aosl_print(*args, **kwargs):
    log(" ".join(args))
print = aosl_print
context.writeln = aosl_print
dpg.create_context()

#LIGHT_IMGUI_THEME = themes.create_theme_imgui_light()
#dpg.bind_theme(LIGHT_IMGUI_THEME)

dpg.create_viewport(title='Athena Operating System 3', width=win_width, height=win_height, clear_color=background)

def fully_destroy(name):
    sub = dpg.get_item_children(name)
    for item in sub:
        for c in sub[item]:
            if dpg.is_item_container(c):
                fully_destroy(c)
            if dpg.does_item_exist(c): dpg.delete_item(c)
    if dpg.does_item_exist(name): dpg.delete_item(name)

def close_win(w, save_pos = True):
    print("start close", w)

    if save_pos:
        context.set_config(f"gui.{w}_pos", dpg.get_item_pos(w))
        context.set_config(f"gui.{w}_width", dpg.get_item_width(w))
        context.set_config(f"gui.{w}_height", dpg.get_item_height(w))
    fully_destroy(w)
    print("Closing", w)
    print(f"win before {WINDOWS}")
    if w in WINDOWS: WINDOWS.remove(w)
    print(f"after {WINDOWS}")

def open_win(w):
    print("Open", w)
    if w not in WINDOWS: 
        WINDOWS.append(w)
        return True
    else:
        return False

def close_log():
    internal_apps["log"]["open"] = False
    fully_destroy("log")

def log(message):
    internal_apps["log"]["buffer"] = message+"\n"+internal_apps["log"]["buffer"]
    if internal_apps["log"]["open"]:
        dpg.set_value("log_text", internal_apps["log"]["buffer"])

def open_log():
    internal_apps["log"]["open"] = True
    with dpg.window(tag="log", label="Log", on_close=close_log, width=400, height=500):
        dpg.add_input_text(multiline=True, width=-1, height=-1, tag="log_text", tracked=True, track_offset=1.0)
        dpg.set_value("log_text", internal_apps["log"]["buffer"])

def open_input(): 
    if dpg.does_alias_exist("aos_input"):
        dpg.focus_item("aos_input_box")
        return

    pos = context.touch_config(f"gui.aos_input_pos", [0, 19])
    height = context.touch_config(f"gui.aos_input_height", 0)
    width = context.touch_config(f"gui.aos_input_width", 0)

    def append_inputlog(message):
        #message = "\n".join(textwrap.wrap(message, 110, replace_whitespace=False))#, replace_whitespace=False))
        message = message.replace(". ", ".\n")
        dpg.set_value("talk_log", message+"\n"+dpg.get_value("talk_log"))

    with dpg.window(label="Input", tag="aos_input", pos = pos, width = width, height = height, on_close = lambda: close_win("aos_input"), horizontal_scrollbar=True):
        def send_talk(**args):
            msg = dpg.get_value("aos_input_box")
            dpg.set_value("talk_log", "> You: "+msg+"\n"+dpg.get_value("talk_log"))
            dpg.set_value("aos_input_box", "")
            dpg.focus_item("aos_input_box")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                try:
                    context.quick_run(msg)
                    append_inputlog(stdout.getvalue())
                except Exception as e:
                    append_inputlog(f"{e}")
                    append_inputlog(traceback.print_exc())

                
            

        with dpg.group(horizontal=True):
            dpg.add_input_text(tag="aos_input_box", width=-45, on_enter=True, callback=lambda: send_talk())
            #dpg.add_key_press_handler(parent="talk_input", callback=lambda: print("done"))
            dpg.add_button(callback=send_talk, label="Send")
        dpg.add_input_text(tag="talk_log", width=-1, height=-1, multiline=True)

def execute_eval():
    text = dpg.get_value(f"textedit_body_eval")
    g = {
        "ctx": context,
        "_dpg": dpg,
        "log": log
    }
    g.update(globals())
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        exec(text, g)
        value = stdout.getvalue()
        log(value)

def aos_popup(message, *, is_prompt = False, is_confirmation = False, callback = None, btn_clipboard = False):
    with dpg.window(tag="aos_popup", modal=True, popup=True, on_close=lambda: close_win("aos_popup")):
        dpg.add_text(message)

        if btn_clipboard:
            dpg.add_button(label="Copy to clipboard", callback=lambda: dpg.set_clipboard_text(message))
        if is_confirmation:
            print("Starting confirmation")
            aos_popup_data["confirmation"] = False
            with dpg.group(horizontal=True):
                def resp(r):
                    aos_popup_data["confirmation"] = r
                    close_win("aos_popup", False)
                    if callback:
                        callback()
                dpg.add_button(label="Yes", callback=lambda: resp(True))
                dpg.add_button(label="No", callback=lambda: resp(False))

def close_imageview(a, b, c):
    if c in internal_apps["imageview"]["open"]:
        internal_apps["imageview"]["open"].remove(c)
    fully_destroy(f"imageview_{c}")


    #dpg.add_dynamic_texture(width=100, height=100, default_value=None, tag="imageview_render")

def open_imageview(fid = 0, path = None):
    print("Open imageview")
    if dpg.does_alias_exist(f"imageview_{fid}"):
        close_win(f"imageview_{fid}", False)

    def open_image(ipath):
        dpg.set_item_label(f"imageview_{fid}", f"Image: {fid} ({ipath})")
        _scale = 10
        width, height, channels, data = dpg.load_image(ipath)
        def redraw(_, scale):
            #scale = new_scale
            if dpg.does_alias_exist(f"imageview_render_{fid}"):
                print("Deleting old render....")
                dpg.delete_item(f"imageview_render_{fid}")

            if dpg.does_alias_exist(f"imageview_img_{fid}"):
                print("Deleting old image....")
                dpg.delete_item(f"imageview_img_{fid}")

            if dpg.does_alias_exist(f"imageview_reg_{fid}"):
                print("Deleting old registry....")
                dpg.delete_item(f"imageview_reg_{fid}")

            with dpg.texture_registry(show=False, tag=f"imageview_reg_{fid}"):
                dpg.add_dynamic_texture(width=width, height=height, default_value=data, tag=f"imageview_render_{fid}")
            
        
            dpg.add_image(f"imageview_render_{fid}", tag=f"imageview_img_{fid}", parent=f"imageview_{fid}", height=height/scale, width=width/scale)

        dpg.add_input_int(min_value=1, default_value=_scale, width=-1, callback=redraw)
        redraw(None, _scale)
        
        #dpg.set_value("imageview_render", data)

    def te_open(*args):
        def opened(_, b):
            spath = list(b['selections'].values())[0]
            print("Open", spath)
            open_image(spath)
            
        with dpg.file_dialog(callback=opened, width=700 ,height=400, directory_selector=False):
            dpg.add_file_extension(".*")
            
    internal_apps["imageview"][f"open"].append(fid)
    label = f"Image: {fid} ({path})"

    with dpg.window(tag=f"imageview_{fid}", label=label, on_close=close_imageview, width=400, height=500, user_data=fid, horizontal_scrollbar=True):
        

        with dpg.menu_bar():
            dpg.add_menu_item(label="Open", callback=te_open)
            with dpg.menu(label="Utilities"):
                dpg.add_menu_item(label="Random Dog", callback=None)
                dpg.add_menu_item(label="Random Cat", callback=None)

        if path:
            open_image(path)


def close_text_edit(a, b, c):
    if c in internal_apps["textedit"]["open"]:
        internal_apps["textedit"]["open"].remove(c)
    fully_destroy(f"textedit_{c}")

def open_text_editor(fid = 0, *, path = None, evaluator = False, readonly = False, allow_saving = True, allow_open = True):
    if dpg.does_alias_exist(f"textedit_{fid}"):
        return

    def te_save(_, b, f):
        p = internal_apps["textedit"][f"{fid}_path"]
        print(b, f, p)

        with open(p, "w+") as fp:
            fp.write(dpg.get_value(f"textedit_body_{f}"))

    def te_open(*args):
        def opened(_, b):
            path = list(b['selections'].values())[0]
            print("Open", path)
            internal_apps["textedit"][f"{fid}_path"] = path
            dpg.set_item_label(f"textedit_{fid}", f"Editor: {fid} ({path})")
            with open(path) as f:
                dpg.set_value(f"textedit_body_{fid}", f.read())
            
        with dpg.file_dialog(callback=opened, width=700 ,height=400, directory_selector=False):
            dpg.add_file_extension(".*")
            
    internal_apps["textedit"][f"open"].append(fid)
    label = f"Editor: {fid} ({path})"
    if readonly: label = label+" READONLY"
    with dpg.window(tag=f"textedit_{fid}", label=label, on_close=close_text_edit, width=400, height=500, user_data=fid):
        with dpg.group(horizontal=True):
            if allow_saving:
                dpg.add_button(label="Save", callback=te_save, user_data=fid)
                dpg.add_button(label="Save As...", callback=lambda: aos_popup("Not yet implemented."))
            
            if allow_open:
                dpg.add_button(label="Open", callback=te_open)

            if evaluator or (path != None and path.endswith(".py")):
                dpg.add_button(label="Evaluate", callback=execute_eval)

        dpg.add_input_text(multiline=True, width=-1, height=-1, tag=f"textedit_body_{fid}", tracked=True, track_offset=1.0, readonly=readonly, enabled=not readonly, tab_input=True)

        internal_apps["textedit"][f"{fid}_path"] = path

        if path:
            if not os.path.exists(path):
                with open(path, "w+") as f:
                    f.write("")

            else:
                with open(path) as f:
                    dpg.set_value(f"textedit_body_{fid}", f.read())

def key(s):
    return keys.get(s, None)

def key_down(a, b, c):
    if dpg.is_key_down(key(context.touch_config("keybinds.input", "F2"))):
        open_input()

    if dpg.is_key_down(key(context.touch_config("keybinds.open_eval", "F5"))):
        if "eval" in internal_apps["textedit"]["open"]:
            execute_eval()
        else:
            #open_eval() 
            open_text_editor("eval", evaluator=True, allow_open=False, path=f"{ATHENAOS_PATH}aos_eval.py")
            #open_text_editor("scratch", path=f"{ATHENAOS_PATH}scratch.txt")

    if dpg.is_key_down(key(context.touch_config("keybinds.open_log", "F6"))):
        if internal_apps["log"]["open"]:
            close_log()
        else:
            open_log()

with dpg.handler_registry():
    dpg.add_key_press_handler(callback=key_down)

def new_text_editor():
    internal_apps["textedit"]["_editors"] += 1
    open_text_editor(internal_apps["textedit"]["_editors"])

def new_imageview(path = None):
    if path == None:
        path = ATHENAOS_PATH+"img/default.jpeg"
    internal_apps["imageview"]["_views"] += 1
    open_imageview(internal_apps["imageview"]["_views"], path)

AOS_VERSION = "a20.04.23 preview"

with dpg.viewport_menu_bar():
    def open_about():
        if dpg.does_alias_exist("aos_about"):
            return
            
        with dpg.window(tag="aos_about", on_close=lambda: close_win("aos_about")):
            dpg.add_text(f"Athena Operating System (Revision 3: {AOS_VERSION})")
            dpg.add_text(f"Created by Technomancer")

            dpg.add_text("\nKeys:")
            for k, v in context.touch_config("keybinds").items():
                dpg.add_text(f"{k} = {v}")

    with dpg.menu(label="System"):
        dpg.add_menu_item(label="New image view", callback=lambda: new_imageview())
        dpg.add_menu_item(label="New editor", callback=lambda: new_text_editor())
        dpg.add_menu_item(label="Input", callback=lambda: open_input(),shortcut=context.touch_config("keybinds.input", "F2"))
        dpg.add_menu_item(label="About", callback=lambda: open_about())
        dpg.add_menu_item(label="Shut down", callback=lambda: dpg.stop_dearpygui())

    with dpg.menu(label="Actions"):
        directory = ATHENAOS_PATH+"actions/"

        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                if filename.split(".")[0] in disabled:
                    continue

                f = os.path.join(directory, filename)
                name = filename.split(".")[0]
                if os.path.isfile(f):
                    f = importlib.import_module("actions."+name)

                    if hasattr(f, "Action"):
                        d = f.Action()
                        d.ctx = context
                        if hasattr(d, "__gui__"):
                            
                            ud = {
                                "label": name, 
                                "dpg":dpg, 
                                "init": open_win, 
                                "close": close_win, 
                                "alert": aos_popup,
                                "context": context,
                                "pos": context.touch_config(f"gui.{name}_pos", [0, 19])
                            }

                            dpg.add_menu_item(label=name, callback=d.__gui__, 
                            user_data=ud)
                            ACTIONS.append(name)
                            if name in autostart or (session_persist and name in last_session):
                                d.__gui__(None, None, ud)

                        if hasattr(d, "__extensions__"):
                            elist = d.__extensions__()
                            if type(elist) == list:
                                for ext in elist:
                                    EXTENSIONS.append(ext)

                    elif hasattr(f, "open_gui"):
                        ud = {
                            "label": name, 
                            "dpg":dpg, 
                            "init": open_win, 
                            "close": close_win,
                            "context": context,
                            "alert": aos_popup
                        }
                        dpg.add_menu_item(label=name, 
                        callback=f.open_gui, 
                        user_data=ud)
                        ACTIONS.append(name)
                        if name in autostart or (session_persist and name in last_session):
                            f.open_gui(None, None, ud)
                    
                    if hasattr(f, "extensions") and type(f.extensions) == list:
                        for ext in f.extensions:
                            EXTENSIONS.append(ext)
        
        if len(EXTENSIONS) > 0:
            dpg.add_separator()

        for item in EXTENSIONS:
            ud = {
                "label": item[0], 
                "dpg": dpg, 
                "init": open_win, 
                "close": close_win, 
                "open_imageview": open_imageview, 
                "open_text_editor": open_text_editor,
                "pos": context.touch_config(f"gui.{item[0]}_pos", [0, 19]),
                "context": context,
                "alert": aos_popup
            }
            print(f"{item}")
            if type(item[1]) == list:
                with dpg.menu(label=item[0]):
                    for subitem in item[1]:
                        dpg.add_menu_item(label=subitem[0], callback=subitem[1], user_data=ud)
            else:
                dpg.add_menu_item(label=item[0], callback=item[1], user_data=ud)

    with dpg.menu(label="Settings"):
        def clear_cache():
            for filename in os.listdir(context.aos_dir+".cache/"):
                print(filename)

        dpg.add_menu_item(label="Save config", callback=lambda: context.save_config())
        dpg.add_menu_item(label="Clear cache", callback=lambda: clear_cache())
        dpg.add_menu_item(label="Open config file", callback=lambda: open_text_editor("config", allow_open=False, path=f"{ATHENAOS_PATH}config.json"))
        dpg.add_menu_item(label="System Style Editor", callback=lambda: dpg.show_style_editor())
        dpg.add_menu_item(label="Evaluator", callback=lambda: open_text_editor("eval", evaluator=True, allow_open=False, path=f"{ATHENAOS_PATH}aos_eval.py"), shortcut=context.touch_config("keybinds.open_eval", "F5"))
        dpg.add_menu_item(label="Log", callback=lambda: open_log(), shortcut=context.touch_config("keybinds.open_log", "F4"))

        def toggle_persist(_, current):
            global session_persist
            print("Persisting", current)
            context.set_config("gui.persist", current)
            session_persist = current

        dpg.add_checkbox(label="Persist Sessions", callback=toggle_persist, default_value=session_persist)
        with dpg.menu(label="Background Colour"):
            def update_background(b):
                b = b[0:3]
                b = [round(base * 255) for base in b]
                print(b)
                dpg.set_viewport_clear_color(b)
                context.set_config("gui.background", b, save=False)

            dpg.add_color_picker(label="Theme", no_alpha = True, callback=lambda _, b: update_background(b), default_value=background)

        with dpg.menu(label="Autostart"):
            def edit_autostart(_, value, name):
                print(value, name)
                if value == True:
                    if name not in autostart:
                        autostart.append(name)
                else:
                    if name in autostart:
                        autostart.remove(name)
                context.set_config("gui.autostart", autostart)

            for act in ACTIONS:
                dpg.add_checkbox(label=act, callback=edit_autostart, default_value=act in autostart, user_data=act)

        with dpg.menu(label="Disable Actions"):
            def edit_disable(_, value, name):
                print(value, name)
                if value == True:
                    if name not in disabled:
                        disabled.append(name)
                else:
                    if name in disabled:
                        disabled.remove(name)

                context.set_config("system.disabled", disabled)
            for act in ACTIONS:
                dpg.add_checkbox(label=act, callback=edit_disable, default_value=act in disabled, user_data=act)
            for act in disabled:
                dpg.add_checkbox(label=act, callback=edit_disable, default_value=act in disabled, user_data=act)

        

    dpg.add_menu_item(label="Help", callback=None)

"""with dpg.window(label="Example Window"):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)"""

dpg.setup_dearpygui()
dpg.show_viewport()
#stdout = io.StringIO()
#with redirect_stdout(stdout):
dpg.start_dearpygui()
    #log(stdout.getvalue())
new_session = []
for win in WINDOWS.copy():
    new_session.append(dpg.get_item_label(win))
    print("ending window", win, dpg.get_item_label(win))
    close_win(dpg.get_item_label(win))

if dpg.does_alias_exist("aos_input"):
    close_win("aos_input")

context.set_config("gui.last_session", new_session)
dpg.destroy_context()
print("AOS shut down.")