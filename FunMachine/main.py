import json
import pyautogui
from filereader import Reader

from enigma.machine import EnigmaMachine
import requests

MORSE_CODE = {"A": ".-",
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
              }
NATO_PHONETIC_ALPHABET = {
    "A": "Alfa",
    "B": "Bravo",
    "C": "Charlie",
    "D": "Delta",
    "E": "Echo",
    "F": "Foxtrot",
    "G": "Golf",
    "H": "Hotel",
    "I": "India",
    "J": "Juliet",
    "K": "Kilo",
    "L": "Lima",
    "M": "Mike",
    "N": "November",
    "O": "Oscar",
    "P": "Papa",
    "Q": "Quebec",
    "R": "Romeo",
    "S": "Sierra",
    "T": "Tango",
    "U": "Uniform",
    "V": "Victor",
    "W": "Whiskey",
    "X": "X-ray",
    "Y": "Yankee",
    "Z": "Zulu"}

API_KEY = "106adff5-c201-4532-b782-86043148a9ec"
RANDOM_URL = "https://api.random.org/json-rpc/4/invoke"
CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"
CHARS_SPECIAL = "ÄÖÜäöü-.,;:_+*#'!?=)[]{}(/&%$§<>|~@€µ"
CHARS_U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def morse():
    text = input("What text do you want to convert to Morse code?: ")
    converted = ' '.join(str(MORSE_CODE[n.upper()]) for n in text if n != " ")
    print(f"Your morse code for '{text}': {converted} ")


def phonetic():
    text = input("What text do you want to convert to the NATO phonetic alphabet?: ")
    phonetic_s = ' '.join(str(NATO_PHONETIC_ALPHABET[n.upper()]) for n in text if n != " ")
    print(f"Your morse code for '{text}': {phonetic_s}")


class Password:
    def __int__(self):
        self.passwords = self.create_password()
        self.print_list(self.passwords)

    @staticmethod
    def create_password():
        password_pool = CHARS + CHARS_U
        length = int(input("How many characters do you need? (1 - 32): ") or 12)
        needed = int(input("How many passwords do you need?: ") or 4)

        if input("Do you need special characters? y/n: ") == "y":
            password_pool += CHARS_SPECIAL
            return random_api(parameters(needed, length, password_pool, "generateStrings"))
        else:
            return random_api(parameters(needed, length, password_pool, "generateStrings"))

    @staticmethod
    def print_list(passwords):
        print([f"PW{i + 1}:\t{pw}" for i, pw in enumerate(passwords)])
        if input("Do you want to save them? (y/n): ") == "y":
            data = '\n'.join(passwords)
            reader.write_passwords(data)


def parameters(n, length, chars, method):
    parameter = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "apiKey": API_KEY,
            "n": n,
            "length": length,
            "characters": chars,
            "replacement": True
        },
        "id": 1
    }
    return json.dumps(parameter)


def parse_response(text):
    data = json.loads(text)
    return data["result"]["random"]["data"]


def random_api(parameter):
    headers = {'Content-type': 'application/json', 'Content-Length': '200', 'Accept': 'application/json'}
    response = requests.post(f"{RANDOM_URL}", data=parameter, headers=headers)
    return parse_response(response.text)


def encrypt(file_encoding):
    global fileencoding
    machine = enigma_setting()
    set_display = random_api(parameters(1, 3, CHARS_U, "generateStrings"))
    machine.set_display(set_display[0])
    if fileencoding:
        text = file_encoding
        print(f"Kenngruppe: {set_display}")
        return machine.process_text(text, replace_char='X')
    else:
        text = input("What text do you need to encrypt?: ")
        encrypted_text = machine.process_text(text, replace_char='X')
        print(f"Encrypted: {encrypted_text}\nKenngruppe: {set_display}")


def decrypt(file_decode):
    global filedecoding
    machine = enigma_setting()
    display_s = input("What was the display setting?: ").upper()
    machine.set_display(display_s)
    if filedecoding:
        decipher = file_decode
        return machine.process_text(decipher, replace_char='X')
    else:
        decipher = input("What was the text you need to decipher?: ")
        decrypted_text = machine.process_text(decipher, replace_char='X')
        print(f"Decrypted: {decrypted_text}\nKenngruppe: {display_s}")


def enigma_setting():
    standardsetting = input("Do you want the standard setting? (y/n): ")
    if standardsetting != "n":
        rot = "II IV V"
        ref = "B"
        ring = [7, 10, 3]
        plug = "AV BS DL FU HZ IN KM OW RX"
    else:
        rot = input("What is the rotor setting? (e.g. II IV V): ") or "II IV V"
        ref = input("What is the reflector setting? (e.g. B): ") or "B"
        ring_s = input("What is the ring settings? (e.g. 7, 10, 3): ") or "7, 10, 3".split(',')
        ring = [int(n) for n in ring_s]
        plug = input("What is the plugboard setting?(e.g. AV BS DL FU HZ IN KM OW RX): ") \
               or "AV BS DL FU HZ IN KM OW RX"
    return EnigmaMachine.from_key_sheet(
        rotors=rot,
        reflector=ref,
        ring_settings=ring,
        plugboard_settings=plug)


def encode_files():
    global reader
    global fileencoding
    fileencoding = True
    files = reader.encode_data
    encoded = []
    for filename, data in files:
        encrypted = encrypt(data)
        encoded.append((filename, encrypted))
        print(f"File '{filename}' encoded!\n")
    reader.write_encoded_files(encoded)
    fileencoding = False


def decode_files():
    global reader
    global filedecoding
    filedecoding = True
    files = reader.decode_data
    decoded = []
    for filename, data in files:
        decrypted = decrypt(data)
        decoded.append((filename, decrypted))
        print(f"File '{filename}' decoded!\n")
    reader.write_decoded_files(decoded)
    filedecoding = False


def start():
    choose = input(
        "\nWhat do you want to do? "
        "\n\t- morse(m) "
        "\n\t- phonetic alphabet(p) "
        "\n\t- password generator(g) "
        "\n\t- encryption(e) "
        "\n\t- encode files(ef)"
        "\n\t- decryption(d)"
        "\n\t- decode files(df)\n")
    if choose == "m":
        morse()
    elif choose == "p":
        phonetic()
    elif choose == "g":
        password_gen = Password()
        passwords = password_gen.create_password()
        password_gen.print_list(passwords)
    elif choose == "e":
        encrypt("")
    elif choose == "ef":
        encode_files()
    elif choose == "d":
        decrypt("")
    elif choose == "df":
        decode_files()


reader = Reader()
firstTime = True
fileencoding = False
filedecoding = False


def continue_i():
    con = input("\n\nDo you want to continue?(y/n): ") or "y"
    if con == "y":
        return True
    return False


def clear_terminal():
    pyautogui.hotkey('ctrl', 'shift', 'alt', 'z')


if firstTime:
    start()
    firstTime = False

while continue_i():
    clear_terminal()
    start()
clear_terminal()
