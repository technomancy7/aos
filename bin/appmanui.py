import dearpygui.dearpygui as dpg
import os, json

all_apps = {}
file_paths = {}
launcher_dir = os.path.dirname(os.path.realpath(__file__))
apps_dir = "/".join(launcher_dir.split("/")[0:-1])+"/data/appman/"
clicked_app = ""
open_file_json = None
open_file_path = None

def append_listbox(name, item):
    items = dpg.get_item_configuration(name)["items"]
    items.append(item)
    dpg.configure_item(name, items=items)

def clear_listbox(name):
    dpg.configure_item(name, items=[])

dpg.create_context()
dpg.create_viewport(title='Appman', width=600, height=600)

def clicked_list(_, name):
    if name.startswith("---"): return
    global clicked_app
    clicked_app = name
    app = all_apps.get(clicked_app)
    dpg.set_value("app_name_input", clicked_app)
    dpg.set_value("app_group_input", app.get("group",""))
    dpg.set_value("app_cmd_input", app.get("command", ""))
    dpg.set_value("display_name", f"Selected: {clicked_app}")
    dpg.set_value("app_desc_input", app.get('description', ""))

def launch_app():
    app = all_apps.get(clicked_app)
    os.system(f"\"{app['command']}\"")

def load_apps():
    displays = {
        "default": []
    }
    clear_listbox("apps")
    for filename in os.listdir(apps_dir):
        with open(apps_dir+filename, "r") as f:
            try:
                data = json.load(f)
                all_apps[filename[:-5]] = data
                if data.get("group", "") == "": 
                    displays["default"].append(filename[:-5])
                else:
                    if displays.get(data["group"], "") == "": 
                        displays[data["group"]] = []
                    displays[data["group"]].append(filename[:-5])
                #append_listbox("apps", filename[:-5])
            except json.JSONDecodeError:
                pass

    for group in displays.keys():
        if group != "default":
            append_listbox("apps", f"--- {group} ---")
            print(displays[group])
            for item in displays[group]:
                append_listbox("apps", item)

    if len(displays["default"]) > 0:
        append_listbox("apps", "--- other apps ---")
        for item in displays["default"]:
            append_listbox("apps", item)

def add_app():
    pass

def delete_app(): pass

def update_app():
    current = all_apps.get(clicked_app)
    current["name"] = dpg.get_value("app_name_input")
    current["group"] = dpg.get_value("app_group_input")
    current["command"] = dpg.get_value("app_cmd_input")
    current["description"] = dpg.get_value("app_desc_input")
    if os.path.exists(apps_dir+clicked_app+".json"):
        os.remove(apps_dir+clicked_app+".json")

    with open(apps_dir+dpg.get_value("app_name_input")+".json", "w+") as f:
        json.dump(current, f)

    load_apps()

with dpg.window(tag="Applications", label="Applications", width=120, height=400):
    with dpg.group(horizontal=True):
        dpg.add_listbox(tag="apps", num_items=30, width=230, callback=clicked_list)
        with dpg.group():
            dpg.add_button(label="Reload", callback=lambda: load_apps())
            dpg.add_button(label="Launch", callback=lambda: launch_app())
            dpg.add_button(label="Delete", callback=lambda: delete_app())
            dpg.add_separator()
            dpg.add_text("Selected: None", tag="display_name")
            with dpg.group():
                dpg.add_input_text(tag="app_name_input", label = "Name", width=290)
                dpg.add_input_text(tag="app_group_input", label = "Group", width=290)
                dpg.add_input_text(tag="app_cmd_input", label = "Command", width=290)
                dpg.add_input_text(tag="app_desc_input", label = "Info", multiline=True, width=290)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Update", callback=lambda: update_app())
                    dpg.add_button(label="Add as new", callback=lambda: add_app())

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Applications", True)
dpg.start_dearpygui()
dpg.destroy_context()