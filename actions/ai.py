import requests
from rich.markdown import Markdown

def generate_content(prompt, api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    params = {
        "key": api_key
    }

    response = requests.post(url, headers=headers, json=data, params=params)

    return response.json()

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "ai",
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
        ln = ctx.get_string()
        ctx.writeln(f"[blue]You[/blue]: {ln}")
        api_key = ctx.touch_config("ai.key")

        if not api_key:
            return ctx.writeln("conf `ai.key` API key missing.")

        resp = generate_content(ln, api_key)
        text = resp['candidates'][0]['content']['parts'][0]['text']

        md = Markdown(text)
        ctx.write_panel(md)

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
