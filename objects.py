import json, os, importlib, textwrap, readline, traceback
from rich.console import Console

class Context:
    def __init__(self, *, line = "", command = "", lines = [], base_dir = ""):
        self.aos_dir = base_dir#ATHENAOS_PATH
        if line != "": self.update_from_line(line)
        else: self.update(command=command, lines=lines)
        #print(lines)
        self.config = {}
        self._exit_code = -1
        self.console = Console(record=True)
        #self.load_config()
        self.plaintext_output = False
        self.buffer = []
        self.time_format = 'HH:mm:ss DD-MM-YYYY'
        self.response = {}

    def coerce_bool(self, line):
        return str(line).lower() in ["1", "yes", "y", "true"]
            
    def update_from_line(self, line):
        line = line.split(" ")
        self.command = line[0]
        self.line = " ".join(line[1:])
        self.lines = line[1:]
        return self

    def update(self, *, command = "", lines = []):
        self.command = command
        self.line = " ".join(lines)
        self.lines = lines
        return self

    def start_response(self):
        self.response = {
            "log": [],
            "data": {},
            "command": self.command,
            "line": self.lines,
            "string": self.get_string()
        }
        self.buffer = self.response["log"]

    def update_response(self, **args):
        self.response["data"].update(**args)

    def clone(self, *, command = "", lines = []):
        c = Context(command=command or self.command, lines = lines or self.lines)
        c.aos_dir = self.aos_dir
        c.load_config()
        c.plaintext_output = self.plaintext_output
        return c

    def execute(self, *, context = None):
        self.start_response()
        subctx = None
        if context == None:
            subctx = self 
        else:
            subctx = context
        
        command = subctx.resolve_alias()

        if not os.path.exists(self.aos_dir+"actions/"+command+".py"):
            return self.writeln(f"Action {command} not found")

        try:
            f = importlib.import_module("actions."+command)
            
            if subctx.get_flag("help") or subctx.get_flag("h"):
                if hasattr(f, "on_help") and type(f.on_help(subctx)) == str:
                    return self.writeln(textwrap.dedent(f.on_help(subctx)))
                return self.writeln(command+" has no help.")
            try:
                if hasattr(f, "on_load"):
                    subctx = f.on_load(subctx) or subctx
            except Exception as e:
                print(traceback.format_exc())
                #print(e)
            finally:
                if hasattr(f, "on_exit"):
                    f.on_exit(subctx)
        except Exception as e:
            print(traceback.format_exc())
        finally:
            if len(subctx.buffer) != 0:
                with open(subctx.aos_dir+"self.log", "a+") as f:
                    f.write("\n--- NEW LOG START ---\n\n")
                    for out in subctx.buffer:
                        f.write(out)
            return subctx

    def resolve_alias(self):
        aliases = self.touch_config("aliases", {})
        for a, realname in aliases.items():
            if a == self.command:
                self.command = realname
                return realname
        return self.command

    def writeln(self, *line, **args):
        self.console.no_color = self.plaintext_output
        self.console.print(*line, **args)
        out = self.console.export_text()
        self.buffer.append(out)

    def ask(self, value, *, prompt = "", default = ""):
        inse = ""
        if prompt != "": inse = f": ({prompt}) "
        f = self.get_flag(value) or input(f"{value}{inse}[{default}] > ")
        if f == "": f = default
        return f

    def has_flag(self, name):
        for flag in self.lines:
            if flag.startswith(f"-{name}:") or flag.startswith(f"--{name}:") and (":" in flag or "=" in flag):
                return True
            if flag == f"-{name}" or flag == f"--{name}" and (":" not in flag and "=" not in flag):
                return True
        return False

    def get_flag(self, name, default = ""):
        for flag in self.lines:
            if flag.startswith(f"-{name}:") or flag.startswith(f"--{name}:") and (":" in flag or "=" in flag):
                if ":" in flag:
                    return flag.split(":")[1]
                elif "=" in flag:
                    return flag.split("=")[1]    
                else:
                    return "true"
            if flag == f"-{name}" or flag == f"--{name}" and (":" not in flag and "=" not in flag):
                return "true"
        return default

    def get_string(self):
        out = []
        for flag in self.lines:
            if not flag.startswith(f"-"):
                out.append(flag)
        return " ".join(out)  

    def get_string_list(self):
        out = []
        for flag in self.lines:
            if not flag.startswith(f"-"):
                out.append(flag)
        return out

    def get_string_ind(self, ind = 0):
        iters = 0
        for flag in self.lines:
            if not flag.startswith(f"-"):
                if iters == ind:
                    return flag
                iters += 1 

    def exit_code(self, newCode = None):
        if newCode == None: return self._exit_code
        self._exit_code = newCode

    def data_path(self, override = ""):
        name = self.command
        if override != "": name = override
        path = self.aos_dir+"data/"+name+"/"
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def open_text_editor(self, default_text = ""):
        txtedit = self.touch_config("system.texteditor", "nano")
        txtfile = self.aos_dir+"editing.txt"

        if not os.path.exists(txtfile):
            f = open(txtfile, "w+")
            f.write(default_text)
            f.close()

        os.system(txtedit+" "+txtfile)
        with open(txtfile, "r") as f:
            return f.read().strip()

    def delete_text_file(self):
        txtfile = self.aos_dir+"editing.txt"
        if os.path.exists(txtfile):
            os.remove(txtfile)

    def validate_data_file(self):
        f = self.data_path()
        if not os.path.exists(f+"data.json"):
            with open(f+"data.json", 'w+') as f:
                f.write("{}")

    def get_data(self):
        f = self.data_path()
        self.validate_data_file()
        with open(f+"data.json", 'r') as fl:
            return json.load(fl)

    def save_data(self, js):
        f = self.data_path()
        self.validate_data_file()
        with open(f+"data.json", 'w+') as fl:
            fl.write(json.dumps(js, indent=4))
        
    def load_config(self):
        if os.path.exists(self.aos_dir+"config.json"):
            with open(self.aos_dir+"config.json", 'r') as f:
                self.config = json.load(f)
                return self.config

    def save_config(self):
        with open(self.aos_dir+"config.json", 'w+') as f:
            f.write(json.dumps(self.config, indent=4))

    def set_config(self, key, value):
        if "." in key:
            parent = key.split(".")[0]
            sub = key.split(".")[1]
            if self.config.get(parent, None) == None:
                self.config[parent] = {}
            
            if type(self.config[parent]) == dict:
                self.config[parent][sub] = value
            else:
                return 

        else:
            self.config[key] = value

        self.save_config()

    def unset_config(self, key):
        if "." in key:
            parent = key.split(".")[0]
            sub = key.split(".")[1]
            if self.config.get(parent, None) == None:
                return
            
            if type(self.config[parent]) == dict:
                del self.config[parent][sub]
            else:
                return 

        else:
            del self.config[key]

        self.save_config()

    def touch_config(self, key, default = None, *, ignore = False, force_refresh = False):
        if force_refresh: self.load_config()
        if "." in key:
            parent = key.split(".")[0]
            sub = key.split(".")[1]
            if self.config.get(parent, None) == None:
                self.config[parent] = {}
            
            if type(self.config[parent]) == dict:
                if self.config[parent].get(sub, None) == None:
                    if not ignore: self.set_config(key, default)
                    return default
                return self.config[parent][sub]
            else:
                return default

        if self.config.get(key, None) == None: self.set_config(key, default)
        return self.config.get(key, default)