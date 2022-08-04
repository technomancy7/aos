import random
import re

class Dataspeak:
    def __init__(self):
        self.tree = []
        self.variables = {}
        self.aphanumeric = re.compile('[\s\W_]+')

    def _strip_input(self, line):
        # @todo Create rules for things like converting don't to do not
        #line = line.lower()
        
        line = ''.join(e for e in line if e.isalnum() or e == " ")

        return line

    def does_trigger_exist(self, trigger):
        for ot in self.tree:
            if trigger == ot["trigger"]:
                return True

        return False

    def get_trigger(self, trigger):
        for ot in self.tree:
            if trigger == ot["trigger"]:
                return ot

        return None

    def delete_trigger(self, trigger):
        for ot in self.tree:
            if trigger == ot["trigger"]:
                self.tree.remove(ot)
                break

    def check_diff(self, original, newone):
        original = self.get_trigger(original)
        #print(newone != original)
        return newone != original

    def add_trigger(self, data):
        self.tree.append(data)

    def load(self, data):
        if data == {}: return
        trigger = data.get("trigger", None)
        responses = data.get("respond", [])
        weight = data.get("weight", 0)
        command = data.get("command", "")
        new_data = {"trigger": trigger, "respond": responses, "weight": int(weight), "command": command}

        if trigger == None:
            #print("A DEFAULT", new_data)
            self.default_response = new_data
            print("Default trigger set...")
            return

        if trigger != None:# and len(responses) > 0:
            #print("checking trigger", trigger, responses)
            to_add = True
            if self.does_trigger_exist(trigger):
                if self.check_diff(trigger, new_data):
                    print("Updating trigger...", trigger, responses)
                    self.delete_trigger(data["trigger"])
                else:
                    to_add = False
            
            if to_add: 
                print("Adding trigger", trigger, responses)
                self.add_trigger(new_data)

    def insert_v(self, line, vars):
        r = re.compile("<\d>")
        tags = r.findall(line)
        #print(tags)
        for tag in tags:
            ind = int(tag[1:-1])
            line = line.replace(tag, vars[ind])
        return line

    def read(self, line):
        line = self._strip_input(line)
        results = []

        for t in self.tree:
            reg = self._check(line, t)
            if reg:
                results.append({"result": t, "regex": reg, "command": self.insert_v(t.get("command", ""), reg)})

        if len(results) == 0:
            response_line = random.choice(self.default_response['respond'])
            return {"text": response_line, "command": ""}

        elif len(results) == 1:
            result = results[0]["result"]
            reg = results[0]["regex"]
            response_line = ""
            if len(result["respond"]) > 0:
                response_line = random.choice(result['respond'])
            return {"text": self.insert_v(response_line, reg), "command": results[0]["command"]}
        
        elif len(results) > 1:
            final_result = None
            current_weight = -1
            for possible in results:
                if possible["result"]["weight"] > current_weight:
                    current_weight = possible["result"]["weight"]
                    final_result = possible
            
            result = final_result["result"]
            reg = final_result["regex"]
            response_line = random.choice(result['respond'])
            return {"text": self.insert_v(response_line, reg), "command": final_result["command"]}
                
                #return random.choice(t['respond'])

    def _check(self, line, part):
        #if line.lower() == part["trigger"]:
            #return True

        #r = re.compile(part["trigger"])
        results = re.findall(part["trigger"], line, re.IGNORECASE)
        #print("results from",part,results)
        if len(results) > 0:
            real_results = []
            #print("pattern match from", part, results)
            for item in results:
                #print(item, type(item))
                if type(item) == tuple:
                    for subitem in item:
                        #print("subitem", subitem)
                        real_results.append(subitem)
                else: real_results.append(item)

            return real_results

        return None

    def export(self):
        return {"tree": self.tree, "variables": self.variables, "default_response": self.default_response}