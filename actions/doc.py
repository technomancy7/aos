import os, json

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "doc",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            Default help.
        """

    def __run__(self, ctx): 
        command, line = ctx.cmdsplit()
        #print(command, "-", line)
        path = ctx.data_path()

        doc = line
        if "." not in doc and "/" not in doc:
            doc = path+doc+".json"
        #print(doc)
        match command:
            case "ls":
                for filename in os.listdir(path):
                    ctx.writeln(f" - {filename.split('.')[0]}")

            case "i" | "info":
                with open(doc) as f:
                    docf = json.load(f)
                    ctx.writeln(f"{docf['name']} ({docf['id']})")
                    ctx.writeln(f"{len(docf['pages'])} pages.")

            case "io" | "iopen":
                print("Interactive open")
            
            case "r" | "read":
                ptr = ctx.get_flag("p") or ctx.get_flag("b") or None
                evalsearch = ctx.get_flag("e")
                textsearch = ctx.get_flag("t")

                with open(doc) as f:
                    docf = json.load(f)

                    if textsearch:
                        for page in docf['pages']:
                            if textsearch in page['text']:
                                ctx.writeln(f"{page['name']} {page['chapter']}:{page['verse']}")
                                ctx.writeln(f"{page['text']}")

                    elif evalsearch:
                        for page in docf['pages']:
                            if eval(evalsearch, {"page": page}):
                                ctx.writeln(f"{page['name']} {page['chapter']}:{page['verse']}")
                                ctx.writeln(f"{page['text']}")

                    elif ptr.isdigit():
                        page = docf['pages'][int(ptr)]
                        ctx.writeln(f"{page['name']} {page['chapter']}:{page['verse']}")
                        ctx.writeln(f"{page['text']}")
                        
                    elif " " in ptr and ":" in ptr:
                        #print(ptr)
                        title = " ".join(ptr.split(" ")[:-1])
                        chapter = ptr.split(":")[0].split(" ")[-1]
                        verse = ptr.split(":")[1]
                        #print("title", title, "chapter", chapter, "verse", verse)
                        for page in docf['pages']:
                            if page['name'] == title and page['chapter'] == chapter and page['verse'] == verse:
                                ctx.writeln(f"{title} {chapter}:{verse}")
                                ctx.writeln(f"{page['text']}")
                            

            case default:
                ctx.writeln(f"Command not understood: {command}")
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

