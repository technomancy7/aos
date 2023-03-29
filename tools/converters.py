
class PhoneButtonConverter:#@todo doesnt work
    def __init__(self):
        self.buttons = {
            '2': 'ABC',
            '3': 'DEF',
            '4': 'GHI',
            '5': 'JKL',
            '6': 'MNO',
            '7': 'PQRS',
            '8': 'TUV',
            '9': 'WXYZ',
            '0': ' ',
        }
        
    def convert(self, numbers):
        result = ''
        for num in numbers:
            if num in self.buttons:
                letters = self.buttons[num]
                result += letters[0]
            else:
                result += num
        return result

class BinaryCoder:
    def encrypt(self, message):
        # return ''.join(format(ord(i), 'b') for i in message)
        return bin(int.from_bytes(message.encode(), "big"))

    def decrypt(self, bits):
        n = int(bits, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, "big").decode()


class MorseCoder:
    def __init__(self):
        self.MORSE_CODE_DICT = {
            "A": ".-",
            "B": "-...",
            "C": "-.-.",
            "D": "-..",
            "E": ".",
            "F": "..-.",
            "G": "--.",
            "H": "....",
            "I": "..",
            "J": ".---",
            "K": "-.-",
            "L": ".-..",
            "M": "--",
            "N": "-.",
            "O": "---",
            "P": ".--.",
            "Q": "--.-",
            "R": ".-.",
            "S": "...",
            "T": "-",
            "U": "..-",
            "V": "...-",
            "W": ".--",
            "X": "-..-",
            "Y": "-.--",
            "Z": "--..",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            "0": "-----",
            ", ": "--..--",
            ".": ".-.-.-",
            "?": "..--..",
            "/": "-..-.",
            "-": "-....-",
            "(": "-.--.",
            ")": "-.--.-",
        }

    # Function to encrypt the string
    # according to the morse code chart

    def encrypt(self, message):
        message = message.upper()
        cipher = ""
        for letter in message:
            if letter != " ":

                # Looks up the dictionary and adds the
                # correspponding morse code
                # along with a space to separate
                # morse codes for different characters
                cipher += self.MORSE_CODE_DICT[letter] + " "
            else:
                # 1 space indicates different characters
                # and 2 indicates different words
                cipher += " "

        return cipher

    # Function to decrypt the string
    # from morse to english
    def decrypt(self, message):
        # extra space added at the end to access the
        # last morse code
        message += " "

        decipher = ""
        citext = ""
        i = 0
        for letter in message:

            # checks for space
            if letter != " ":

                # counter to keep track of space
                i = 0

                # storing morse code of a single character
                citext += letter

            # in case of space
            else:
                # if i = 1 that indicates a new character
                i += 1

                # if i = 2 that indicates a new word
                if i == 2:

                    # adding space to separate words
                    decipher += " "
                else:

                    # accessing the keys using their values (reverse of encryption)
                    decipher += list(self.MORSE_CODE_DICT.keys())[
                        list(self.MORSE_CODE_DICT.values()).index(citext)
                    ]
                    citext = ""

        return decipher
