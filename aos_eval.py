import re

text = "This is some [example] text with [square brackets] in it"
regex_pattern = r'\[([^\]]+)\]'
matches = re.findall(regex_pattern, text)

print(matches)




## lol