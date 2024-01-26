import requests, os, base64
import urllib.parse

class VirusTotal:
    def __init__(self, key):
        self.key = key

    def search(self, query):
        url = f"https://www.virustotal.com/api/v3/search?query={query}"

        headers = {
            "accept": "application/json",
            "x-apikey": self.key,
        }

        #print(f"Scanning '{target}'")
        response = requests.get(url, headers=headers).json()
        #print(response)
        return response['data']

    def scan_file(self, filepath):
        filename = os.path.basename(filepath)
        url = "https://www.virustotal.com/api/v3/files"

        with open(filepath, 'rb') as f:
            #print(f"Scanning {filepath} ({filename}) at {self.key}")
            files = {"file": (filename, f)}
            headers = {
                "accept": "application/json",
                "x-apikey": self.key
            }

            response = requests.post(url, files=files, headers=headers).json()
            anid = response['data']['id']
            return anid

    def scan_url(self, target):
        target = urllib.parse.quote(target, safe='')
        url = "https://www.virustotal.com/api/v3/urls"


        payload = f"url={target}"

        headers = {
            "accept": "application/json",
            "x-apikey": self.key,
            "content-type": "application/x-www-form-urlencoded"
        }

        #print(f"Scanning '{target}'")
        response = requests.post(url, data=payload, headers=headers).json()
        #print(response)
        anid = response['data']['id']
        return anid

    def analysis(self, id):
        url = f"https://www.virustotal.com/api/v3/analyses/{id}"
        headers = {
            "accept": "application/json",
            "x-apikey": self.key
        }
        response = requests.get(url, headers=headers).json()
        return response