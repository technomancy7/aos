from tools.pymachine import PYM

state = PYM()
print(state.objects)
print("getting player", state.get(id = "player", name = "Borker"))
print("getting first zone", state.get(object_type = "zone"))

print("getting player", state.get_match(id = "end", name = ""))
print("all zones", state.find(object_type = "zone"))
print(state.current())
print(state.commands)