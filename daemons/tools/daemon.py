import os, json, shlex
from subprocess import Popen, PIPE

HOME = os.path.expanduser("~")+"/"
ATHENAOS_PATH = HOME+".aos/"

class Context:
    def __init__(self, id):
        self.id = id
        self.home = HOME
        self.aos_dir = ATHENAOS_PATH
        self._exit_code = -1

    def new_proc(self, command, name):
        with open(self.aos_dir+name+".log", "w+") as f:
            p =  Popen(shlex.split(command), stdout=f)
            d = self.get_data()

            d["procs"][name] = {
                "command": command,
                "name": name,
                "stdout": self.aos_dir+name+".log",
                "pid": p.pid
            } 
            self.save_data(d)

    def alive(self):
        return True

    def exit_code(self, newCode = None):
        if newCode == None: return self._exit_code
        self._exit_code = newCode

    def data_path(self):
        path = self.aos_dir+"data/"+self.id+"/"
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def validate_data_file(self):
        f = self.data_path()
        if not os.path.exists(f+"data.json"):
            with open(f+"data.json", 'w+') as f:
                f.write("{}")
        return f

    def get_data(self):
        f = self.validate_data_file()
        with open(f+"data.json", 'r') as f:
            return json.load(f)

    def save_data(self, js):
        f = self.validate_data_file()
        with open(f+"data.json", 'w+') as f:
            f.write(json.dumps(js, indent=4))
        
    def load_config(self):
        if os.path.exists(self.aos_dir+"config.json"):
            with open(self.aos_dir+"config.json", 'r') as f:
                self.config = json.load(f)
                return self.config

    def save_config(self):
        with open(self.aos_dir+"config.json", 'w+') as f:
            f.write(json.dumps(self.config, indent=4))