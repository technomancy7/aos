import re
import textwrap
import io
import traceback
from contextlib import redirect_stdout

def PreProc_Reform(engine, body):
    for line in body.split("\n"):
        if line.startswith("start") and "<<" in line:
            edit = line.replace("<<", "\n<<")
            body = body.replace(line, edit)

    return body

def PreProc_Label(engine, body):
    v = engine.setv
    g = engine.getv

    v("_lineno", 0) 
    for line in body.split("\n"):
        v("_lineno", int(g("_lineno"))+1) 
        if line.startswith(":"):
            labelname = line[1:]
            engine.variables["_labels"][labelname] = int(g("_lineno")) 
        

    v("_lineno", -1)         
    return body

class InfoscriptBase:
    @staticmethod
    def extend(engine):
        engine.commands["echo"] = InfoscriptBase.echo
        engine.commands["get"] = InfoscriptBase.getv
        engine.commands["set"] = InfoscriptBase.setv
        engine.commands["append"] = InfoscriptBase.appendv
        engine.commands["remove"] = InfoscriptBase.unappendv
        engine.commands["test"] = InfoscriptBase.test
        engine.commands["eval"] = InfoscriptBase._eval
        engine.commands["exec"] = InfoscriptBase._exec
        engine.commands["input"] = InfoscriptBase._input

    @staticmethod
    def _input(engine, line):
        return input(line+"?>")

    @staticmethod
    def _eval(engine, line):
        return engine._eval(line)

    @staticmethod
    def _exec(engine, line):
        return engine._exec(line)

    @staticmethod
    def getv(engine, line):
        #print(line)
        return engine.getv(line)

    @staticmethod
    def setv(engine, line):
        engine.setv(line.split(" ")[0], " ".join(line.split(" ")[1:]))

    @staticmethod
    def appendv(engine, line):
        engine.appendv(line.split(" ")[0], " ".join(line.split(" ")[1:]))

    @staticmethod
    def unappendv(engine, line):
        engine.unappendv(line.split(" ")[0], " ".join(line.split(" ")[1:]))

    @staticmethod
    def test(engine, line):
        if line == "": line = "success"
        return f"TEST:{line}!!!"

    @staticmethod
    def echo(engine, line):
        line = engine._handle(line)
        engine.echo(line)

class Datascript:
    @staticmethod
    def from_file(path):
        with open(path, "r") as f:
            parser = Datascript()
            parser.parse(f.read())
            return parser

    @staticmethod
    def from_text(text):
        parser = Datascript()
        parser.parse(text)
        return parser

    def echo(self, line):
        blck = ""
        if self.getv("_current_block", "") != "":
            blck = ":"+self.getv("_current_block", "")
        self.writeln(f'({self.getv("_lineno")}{blck}) {line}')

    def _handle(self, line):
        if type(line) != str: return line
        #print(f"Handle {line} {type(line)}")
        #reg = re.compile("\`[\w\W]*\`")
        if line.startswith("`") and line.endswith("`"):
            return self._eval(line[1:-1])

        reg = re.compile("\@{[\w_\-\.\[\]\d\"\'\#]*}")
        for word in reg.findall(line):
            #print(f"Found {word}")
            line = line.replace(word, str(self.getv(word[2:-1])))

        regc = re.compile("\#{[\w_\-\.:\s\[\]\d\"\']*}")
        for word in regc.findall(line):
            modified_word = word[2:-1]
            result = ""
            if ":" in modified_word:
                cmd = modified_word.split(":")[0]
                cmdln = ":".join(modified_word.split(":")[1:]).strip()   
                if self.commands.get(cmd, None) != None:
                    result = self.commands[cmd](self, line=cmdln)
                    
            else:
                if self.commands.get(modified_word, None) != None:
                    result = self.commands[modified_word](self, line="")

            line = line.replace(word, str(result))

        return line

    def _exec(self, line):
        try:
            result = exec(line, self.env)
            return result
        except Exception as e:
            print(e)
            tb = traceback.format_exc()
            print(tb)
            return "ERROR"

    def _eval(self, line):
        try:
            result = eval(line, self.env)
            return result
        except Exception as e:
            print(e)
            tb = traceback.format_exc()
            print(tb)
            return "ERROR"

    def __init__(self):
        self.writeln = print
        self.body = ""
        self.data = {}
        self.variables = {
            "_number_of_blocks": 0,
            "_version": "0test",
            "_current_block": "",
            "_lineno": 0,
            "_labels": {}
        }
        self.commands = {}

        self.preprocessors = [
            PreProc_Reform,
            PreProc_Label
        ]

        InfoscriptBase.extend(self)
        self.env = {
            "_": self,
            "_vars": self.variables,
            "_version": self.getv("_version"),
            "setv": self.setv,
            "getv": self.getv,
            "appendv": self.appendv,
            "unappendv": self.unappendv
        }

    def setv(self, key, val):
        val = self._handle(val)
        if "." in key:
            parent = self._handle(key.split(".")[0])
            sub = self._handle(key.split(".")[1])
            
            if self.variables.get(parent, None) == None:
                self.variables[parent] = {}
            self.variables[parent][sub] = val
        else:
            self.variables[self._handle(key)] = val

    def appendv(self, key, val):
        val = self._handle(val)
        l = self.getv(key, [])
        if type(l) != list:
            return print(f"{key} value not a list, can't operate.")
        else:
            l.append(val)
            self.setv(key, l)

    def unappendv(self, key, val):
        val = self._handle(val)
        l = self.getv(key, [])
        if type(l) != list:
            return print(f"{key} value not a list, can't operate.")
        else:
            l.remove(val)
            self.setv(key, l)

    def getv(self, key, default = None):
        if "." in key:
            parent = self._handle(key.split(".")[0])
            sub = self._handle(key.split(".")[1])
            if self.variables.get(parent, None) == None:
                return default
                
            if "#" in sub:        
                ind = int(sub.split("#")[1])
                return self.variables[parent].get(self._handle(sub).split("#")[0], [])[ind]
            else:
                return self.variables[parent].get(self._handle(sub), default)
        else:
            if "#" in key: 
                ind = int(key.split("#")[1])
                key = key.split("#")[0]
                return self.variables.get(self._handle(key), [])[ind]
            else:
                return self.variables.get(self._handle(key), default)

    def readline(self, line):
        v = self.setv
        g = self.getv
        
        if line.startswith("//"): return

        if g("_current_block") == "":
            if line.startswith("start"):
                if " " in line:
                    v("_current_block", " ".join(line.split(" ")[1:]))
                else:
                    name = 'block_'+str(g("_number_of_blocks"))
                    v("_current_block", name)
                v("_number_of_blocks", int(g("_number_of_blocks"))+1)  

            if line.startswith("@"):
                key = line.split(" ")[0][1:]
                val = " ".join(line.split(" ")[1:])
                v(key, val)
            
            if line.startswith("#"):
                cmd = line.split(" ")[0][1:]
                val = " ".join(line.split(" ")[1:])
                if self.commands.get(cmd, None) != None:
                    self.commands[cmd](self, line=val)

            if line.startswith("+"):
                key = line.split(" ")[0][1:]
                val = " ".join(line.split(" ")[1:])
                self.appendv(key, val)
        else:
            if line == "end":
                v("_current_block", "")
            else:
                b = g("_current_block")
                if line.startswith("<<"):
                    block_name = line[2:]
                    toimport = self.getv(block_name)
                    for k, val in toimport.items():
                        v(b+"."+k, val)

                if line.startswith("@"):
                    key = line.split(" ")[0][1:]
                    val = " ".join(line.split(" ")[1:])
                    v(b+"."+key, val)

                if line.startswith("+"):
                    key = line.split(" ")[0][1:]
                    val = " ".join(line.split(" ")[1:])
                    self.appendv(b+"."+key, val)

                if line.startswith("#"):
                    cmd = line.split(" ")[0][1:]
                    val = " ".join(line.split(" ")[1:])

                    if self.commands.get(cmd, None) != None:
                        self.commands[cmd](self, line=val)

    def parse_file(self, path):
        with open(path, "r") as f:
            return self.parse(f.read())

    def parse(self, body):
        v = self.setv
        g = self.getv

        for preproc in self.preprocessors:
            body = preproc(self, body)

        v("_current_block", "")
        v("_lineno", 0) 
        all_lines = body.split("\n")

        #for linen in range(0, len(all_lines)):
        while True:
            if g("_lineno", 0) >= len(all_lines): break
            if all_lines[g("_lineno", 0)] == "stop": break
            line = all_lines[g("_lineno", 0)].strip()
            self.readline(line)
            v("_lineno", int(g("_lineno"))+1) 
            
        
        v("_current_block", "")
        v("_lineno", -1) 
        v("_line_count", len(all_lines))

        return {
            "variables": self.variables
        }

            

