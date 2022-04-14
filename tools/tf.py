import subprocess

_help = """
        The GNU Talk Filters are filter programs that convert ordinary English text into text that mimics a stereotyped or otherwise humorous dialect.  
        
        tf <name> <message>

        NAME             DESCRIPTION
        -------------------------------------------------------------
        austro           Austrian accent (Ahhhnold)
        b1ff             B1FF of USENET yore
        brooklyn         Brooklyn accent
        chef             Swedish Chef (from The Muppet Show)
        cockney          Londoner accent
        drawl            Southern drawl
        dubya            George "Dubya" Bush
        fudd             Elmer Fudd (from the Looney Tunes cartoons)
        funetak          Thick Asian accent
        jethro           Jethro from The Beverly Hillbillies
        jive             1970s Jive
        kraut            German accent
        pansy            Effeminate male
        pirate           Pirate talk
        postmodern       Postmodernist talk ("Feminazi")
        redneck          Country redneck
        valspeak         Valley talk
        warez            H4x0r code
"""
class TalkFilterRuntimeError(Exception):
    pass

def print_filters():
    print(_help)
    
def filter_info():
    return _help
    
def list_filters():
    return ['austro', 'b1ff', 'brooklyn', 'chef', 'cockney', 'drawl', 'dubya', 'fudd', 'funetak', 'jethro', 'jive', 'kraut', 'pansy', 'pirate', 'postmodern', 'redneck', 'valspeak', 'warez']
        
def send(filter_name, text, path=""):
    if filter_name not in list_filters():
        raise ValueError(f"Talkfilter {filter_name} not found.")
    
    tf = subprocess.Popen([path+filter_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = tf.communicate(input=text)
    if errors:
        raise TalkFilterRuntimeError(str(errors))
    return output

