import json, requests, os, webbrowser

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "misc",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "description": "A collection of misc built-in actions.",
            "group": "",
        }

    def download(self, url, download_to = None):
        if download_to == None: download_to = self.ctx.aos_dir+".cache/"
        filename = url.split("/")[-1]
        r = requests.get(url)  
        path = os.path.join(download_to, filename)
        with open(path, 'wb') as fd:
            fd.write(r.content)
        return path

    def get_lyrics(self, title):
        url = f"https://some-random-api.ml/lyrics?title={title.replace(' ', '+')}"
        return requests.get(url).json()

    def define(self, word):
        return requests.get(f"https://some-random-api.ml/others/dictionary?word={word}").json()

    def random_dog2(self):
        url = "https://random.dog/woof.json"
        return requests.get(url).json().get("url", None)

    def random_dog(self):
        url = "https://some-random-api.ml/animal/dog"
        return requests.get(url).json()

    def random_cat2(self):
        url = "https://api.thecatapi.com/v1/images/search"
        headers={"x-api-key": "dca2da26-0ed8-406b-a99d-b8e86d165c99"}
        return requests.get(url, headers=headers).json()[0].get("url", None)

    def random_cat(self):
        url = "https://some-random-api.ml/animal/cat"
        return requests.get(url).json()

    def random_joke(self):
        return requests.get("https://some-random-api.ml/others/joke").json().get("joke", "None")
    
    def random_dogfact_gui(self, _, d, data):
        data['alert'](self.random_dog().get("fact", "None"))

    def random_catfact_gui(self, _, d, data):
        data['alert'](self.random_cat().get("fact", "None"))

    def myip_gui(self, _, d, data):
        data['alert'](requests.get('https://api.ipify.org').text, btn_clipboard=True)

    def random_joke_gui(self, _, d, data):
        data['alert'](self.random_joke())

    def random_dog_gui(self, _, d, data):
        dog = self.random_dog()['image']
        path = self.download(dog)
        data['open_imageview']("dog", path)

    def random_cat_gui(self, _, d, data):
        cat = self.random_cat()['image']
        path = self.download(cat)
        data['open_imageview']("cat", path)

    def define_gui(self, _, d, data):
        dpg = data['dpg']
        label = data['label']
        context = data['context']
        pos = context.touch_config(f"gui.{label}_pos", [0, 19])
        height = context.touch_config(f"gui.{label}_height", 0)
        width = context.touch_config(f"gui.{label}_width", 0)

        with dpg.window(label=label, tag=label, on_close = lambda: data["close"](label), pos = pos, width = width, height = height):
            def send_talk(**args):
                word = dpg.get_value("define_input")
                results = self.define(word)
                if results.get("error"):
                    dpg.set_value("define_output", results['error'])
                else:
                    defin = results['definition'].replace(". ", ".\n")
                    dpg.set_value("define_output", f"{defin}")
                dpg.focus_item("define_input")

            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="define_input", width=-45, on_enter=True, callback=lambda: send_talk())
                dpg.add_button(callback=send_talk, label="Send")

            dpg.add_input_text(tag="define_output", width=-1, height=-1, multiline=True)

    def lyrics_gui(self, _, d, data):
        dpg = data['dpg']
        label = data['label']
        context = data['context']
        pos = context.touch_config(f"gui.{label}_pos", [0, 19])
        height = context.touch_config(f"gui.{label}_height", 0)
        width = context.touch_config(f"gui.{label}_width", 0)

        with dpg.window(label=label, tag=label, on_close = lambda: data["close"](label), pos = pos, width = width, height = height):
            def send_talk(**args):
                song_title = dpg.get_value("lyrics_input")
                results = self.get_lyrics(song_title)
                if results.get("error"):
                    dpg.set_value("lyrics_output", results['error'])
                else:
                    author = results['author']
                    song = results['title']
                    lyr = results['lyrics']
                    dpg.set_value("lyrics_output", f"{song} by {author}\n{lyr}")
                dpg.focus_item("lyrics_input")

            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="lyrics_input", width=-45, on_enter=True, callback=lambda: send_talk())
                dpg.add_button(callback=send_talk, label="Send")

            dpg.add_input_text(tag="lyrics_output", width=-1, height=-1, multiline=True)

    def __run__(self, ctx): 
        cmd, ln = ctx.cmdsplit()

        match cmd:
            case "ip" | "myip":
                ip = requests.get('https://api.ipify.org').text
                ctx.writeln(f'Your IP address is: {ip}')

            case "download" | "dl":
                td = ctx.get_flag("o") or None
                self.download(ln, td)

            case "joke":
                joke = self.random_joke()
                ctx.writeln(joke)
           
            case "dog":
                dog = self.random_dog()['image']
                webbrowser.open(dog)

            case "dogfact" | "df":
                dog = self.random_dog()['fact']
                ctx.writeln(dog)

            case "cat":
                cat = self.random_cat()['image']
                webbrowser.open(cat)

            case "catfact" | "cf":
                cat = self.random_cat()['fact']
                ctx.writeln(cat)

            case "define" | "def" | "d":
                d = self.define(ln)
                if d.get("error"):
                    return ctx.writeln(d['error'])
                else:
                    ctx.writeln(d["definition"])

            case "lyrics" | "lyr" | "l":
                results = self.get_lyrics(ln)
                if results.get("error"):
                    return ctx.writeln(results['error'])
                else:
                    author = results['author']
                    song = results['title']
                    lyr = results['lyrics']
                    ctx.writeln(f"{song} by {author}\n{lyr}")
                    

    def __extensions__(self):
        return [
            [   
                "Animals", 
                [
                    ["Random Dog", self.random_dog_gui],
                    ["Random Cat", self.random_cat_gui],
                    ["Random Dog Fact", self.random_dogfact_gui],
                    ["Random Cat Fact", self.random_catfact_gui],
                ]
            ],
            ["Random Joke", self.random_joke_gui],
            ["Define Word", self.define_gui],
            ["Lyrics", self.lyrics_gui],
            ["Display IP addr", self.myip_gui]
        ]