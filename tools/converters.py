
class XConverter:
    def __init__(self):
        self.temps = ["k", "f", "c"]
        self.weights = ["mg", "g", "kg", "oz", "lb"]
        self.distances = ["m", "cm", "mm", "km", "inch", "ft", "yd", "mile"]
        self.translation_table = {
            "m": "meters",
            "cm": "centimeters",
            "mm": "milimeters",
            "km": "kilometers",
            "inch": "inches",
            "ft": "feet",
            "yd": "yards",
            "mile": "miles",

            "mg": "milligrams",
            "g": "grams",
            "kg": "kilograms",
            "oz": "ounces",
            "lb": "pounds",

            "k": "kelvin",
            "f": "fahrenheit",
            "c": "celcius",
        }

    def pretty_convert(self, base_value, base_type, to_type):
        value = self.convert(base_value, base_type, to_type)
        str_base_type = self.translation_table.get(base_type, base_type)
        str_to_type = self.translation_table.get(to_type, to_type)
        return f"{base_value} {str_base_type} is {value:.2f} {str_to_type}"

    def convert(self, base_value, base_type, to_type):
        base_value = int(base_value)

        if base_type in self.temps and base_type in self.temps:
            return self.convert_temp(base_value, base_type, to_type)

        if base_type in self.weights and base_type in self.weights:
            return self.convert_weight(base_value, base_type, to_type)

        if base_type in self.distances and base_type in self.distances:
            return self.convert_dist(base_value, base_type, to_type)

    def convert_temp(self, base_value, base_type, to_type):
          if base_type == "c" and to_type == "f":
              result = (base_value * 9/5) + 32
              return result

          elif base_type == "f" and to_type == "c":
              result = (base_value - 32) * 5/9
              return result

          elif base_type == "c" and to_type == "k":
              result = base_value + 273.15
              return result

          elif base_type == "k" and to_type == "c":
              result = base_value - 273.15
              return result

          elif base_type == "f" and to_type == "k":
              result = (base_value - 32) * 5/9 + 273.15
              return result

          elif base_type == "k" and to_type == "f":
              result = (base_value - 273.15) * 9/5 + 32
              return result

    def convert_weight(self, base_value, base_type, to_type):
        base_value = int(base_value)
        conversion_factors = {
            "mg": 0.001,
            "g": 1,
            "kg": 1000,
            "oz": 28.3495,
            "lb": 453.592
        }

        if base_type in conversion_factors and to_type in conversion_factors:
            factor_in = conversion_factors[base_type]
            factor_out = conversion_factors[to_type]

            return base_value * factor_in / factor_out

        else:
            raise ValueError("Invalid units")

    def convert_dist(self, base_value, base_type, to_type):
        base_value = int(base_value)
        conversion_factors = {
            'm': 1.0,
            'cm': 0.01,
            'mm': 0.001,
            'km': 1000.0,
            'inch': 0.0254,
            'ft': 0.3048,
            'yd': 0.9144,
            'mile': 1609.34
        }

        if base_type in conversion_factors and to_type in conversion_factors:
            factor_in = conversion_factors[base_type]
            factor_out = conversion_factors[to_type]

            return base_value * factor_in / factor_out

        else:
            raise ValueError("Invalid units")



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
