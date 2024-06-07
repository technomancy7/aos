import json, requests, os, webbrowser

#TODO need new apis for the animals

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

        return ctx
