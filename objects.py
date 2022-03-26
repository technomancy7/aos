import json, os
from rich.console import Console

class Context:
    def __init__(self, *, command = "", line = "", lines = []):
        self.aos_dir = ""#ATHENAOS_PATH
        self.command = command
        self.line = line
        self.lines = lines
        #print(lines)
        self.config = {}
        self._exit_code = -1
        self.console = Console(record=True)
        #self.load_config()
        self.plaintext_output = False

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
        with open(self.aos_dir+"self.log", "a+") as f:
            f.write(out)

    def ask(self, value, *, prompt = "", default = ""):
        inse = ""
        if prompt != "": inse = f": ({prompt}) "
        f = self.get_flag(value) or input(f"{value}{inse}[{default}] > ")
        if f == "": f = default
        return f

    def has_flag(self, name):
        for flag in self.lines:
            if flag.startswith(f"-{name}") or flag.startswith(f"--{name}") and (":" in flag or "=" in flag):
                return True
            if flag == f"-{name}" or flag == f"--{name}" and (":" not in flag and "=" not in flag):
                return True

    def get_flag(self, name):
        for flag in self.lines:
            if flag.startswith(f"-{name}") or flag.startswith(f"--{name}") and (":" in flag or "=" in flag):
                if ":" in flag:
                    return flag.split(":")[1]
                elif "=" in flag:
                    return flag.split("=")[1]    
                else:
                    return "true"
            if flag == f"-{name}" or flag == f"--{name}" and (":" not in flag and "=" not in flag):
                return "true"
        return ""

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

    def touch_config(self, key, default = None):
        self.load_config()
        if "." in key:
            parent = key.split(".")[0]
            sub = key.split(".")[1]
            if self.config.get(parent, None) == None:
                self.config[parent] = {}
            
            if type(self.config[parent]) == dict:
                if self.config[parent].get(sub, None) == None:
                    self.set_config(key, default)
                    return default
                return self.config[parent][sub]
            else:
                return default
        if self.config.get(key, None) == None: self.set_config(key, default)
        return self.config.get(key, default)