import re, aiohttp, requests

class GSMaster:
    def __init__(self):
        self.servers = []
        self.server_count = 0
        self.players = 0
        self.game = ""
        self.real_total = 0

        self.protocol = "333networks"
        
        self.hosts_list = {
            "333networks": "https://master.333networks.com/json/$g",
            "333networks-2k4": "https://ut2004master.333networks.com/json/ut2004"
        }

        self.hosts_server = {
            "333networks": "https://master.333networks.com/json/$g/$h",
            "333networks-2k4": "https://ut2004master.333networks.com/json/ut2004/$h"
        }

        self.host_overrides = {
            "ut2004": "333networks-2k4"
        }
        
        self.server_class = {
            "333networks": uServer,
            "333networks-2k4": uServer
        }

    def get_url(self):
        return self.hosts_list[self.protocol].replace("$g", self.game)

    def get_server_url(self, host):
        return self.hosts_server[self.protocol].replace("$g", self.game).replace("$h", host)

    def reset(self):
        self.servers.clear()
        self.server_count = 0
        self.players = 0  
        self.real_total = 0

    def errored_server(self):
        data = {
                "ip": "error",
                "hostname": "not_found",
                "numplayers": -1,
                "maxplayers": -1,
                "country": None
            }
        return uServer(data, True)

    async def get(self, game, params={}):
        self.game = game
        if game in self.host_overrides.keys():
            self.protocol = self.host_overrides[game]

        url = self.get_url()
        self.reset()
        

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, data={'User-Agent': 'Athena'}) as r:
                try:
                    data = await r.json()
                except:
                    data = {"error": 999}

                if type(data) == dict and data.get("error", 0) >= 1:
                    return None

                if len(data[0]) == 0:
                    return None
                    
                for sv in data[0]:
                    self.server_count += 1
                    self.servers.append(self.server_class.get(self.protocol, uServer)(sv, True))

                self.players = data[1]["players"]
                self.real_total = data[1]["total"]

        return self.servers

    async def get_server(self, host, game = "", params={}):
        if game != "": self.game = game
        if game == "": game = self.game

        if game in self.host_overrides.keys():
            self.protocol = self.host_overrides[game]

        url = self.get_server_url(host)

        self.reset()

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, data={'User-Agent': 'Athena'}) as r:
                try:
                    data = await r.json()
                except:
                    return self.errored_server()

                return self.server_class.get(self.protocol, uServer)(data, False)          

class uServer:
    def __init__(self, data, partial):
        self.json = data
        self.partial = partial
        for key, val in data.items():
            #if key == "queryport" or key == "port": key = "hostport"

            if key == "hostname" or key == "mapname":
                #val = val.encode("ascii", "ignore").decode()
                val = re.sub(r'[^\x00-\x7f]', "", val)
                val = ''.join([m if ord(m) < 128 else ' ' for m in val])
            setattr(self, key, val)