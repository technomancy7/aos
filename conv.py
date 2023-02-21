import os, textwrap

for filename in os.listdir("actions"):
    print(filename)
    with open(filename, "r") as f:
        text = f.read()
        textwrap.indent(text, "    ")
        text = f"""
class {filename.split('.')[0]}:
    {text}      
        """
    print(text)
    break

