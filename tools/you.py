import requests

class You:
    def __init__(self, key):
        self.key = key
        
        self.MODEL_YOUDOTCOM = "youdotcom/chat"
        self.MODEL_BETTERCHAT = "betterapi/betterchat"
        self.MODEL_BARD = "google/bard"

        self.chatmodel = self.MODEL_YOUDOTCOM

    def chat(self, ln):
        output = ""
        url = f"https://api.betterapi.net/{self.chatmodel}?message={ln}&key={self.key}" 
        #print(url)
        r = requests.get(url)

        try:
            j = r.json()
            output = j["message"]
        except:
            output = f"{r} {r.content}"

        return output

    def imagine(self, ln):
        #print(self.key)
        url = f"https://api.betterapi.net/youdotcom/imagine?message={ln}&key={self.key}" 
        r = requests.get(url)#.json()

        try:
            j = r.json()
            output = j['image_url']
        except:
            output = f"{r} {r.content}"
        return output
