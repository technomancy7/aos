from datetime import datetime
import re
class Action:
    @staticmethod
    def __action__():
        return {
            "name": "rk",
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

    def dts(self, time_string):
        """
        Converts a string in the format "hh:mm:ss day/month/year" to a datetime object.

        :param time_string: A string in the format "hh:mm:ss day/month/year"
        :return: A datetime object
        """
        try:
            # Parse the string into a datetime object
            return datetime.strptime(time_string, "%H:%M:%S %d/%m/%Y")
        except ValueError as e:
            print(f"Error parsing the date string: {e}")
            return None

    def nows(self):
        """
        Returns the current time as a string in the format "hh:mm:ss day/month/year".
        """
        now = datetime.now()
        return now.strftime("%H:%M:%S %d/%m/%Y")

    def remove_words(self, text, words_to_remove):
        pattern = '|'.join(map(re.escape, words_to_remove))
        text = re.sub(r'\b(' + pattern + r')\b', '', text, flags=re.IGNORECASE)
        return re.sub(r'\s+', ' ', text).strip()

    def extract_tags(self, text):
        """
        Extracts all words beginning with '#' from the given text.

        :param text: The input string to search for hashtags.
        :return: A list of hashtags found in the text.
        """
        # Use a regular expression to find all words starting with '#'
        hashtag_pattern = r'#\w+'
        print(text)
        hashtags = re.findall(hashtag_pattern, text)
        print("ht", hashtags)
        return self.remove_words(text, hashtags), hashtags

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()
        # Main functionality here.

        match cmd:
            case "add" | "new" | "a":
                d = ctx.get_data()
                if not d.get("entries"): d["entries"] = []
                #txt, tags = self.extract_tags(ln)
                d['entries'].append({
                    "timestamp": self.nows(),
                    "text": ln
                })

                ctx.save_data(d)


            case "list" | "ls":
                d = ctx.get_data()
                for idx, item in enumerate(d.get("entries", [])):
                    ctx.writeln(f"# {idx} {item['timestamp']}: {item['text']}")
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
