# std
import base64
import sys
# 3rd party
from Crypto.Cipher import AES
# local
import config


base64encode = base64.encodebytes if sys.version_info.major >= 3 else base64.encodestring
base64decode = base64.decodebytes if sys.version_info.major >= 3 else base64.decodestring


secret_key = b'\x03\xf2\x15\xe7`\xebd\x9e[7v14\x14.C'
cipher = AES.new(secret_key, AES.MODE_ECB)


def pad(word, n, pad_char):
    """
    Pad the given word with the pad character so that the length is a multiple
    of n.

    :param word: str|bytes - The word to pad.
    :param n: int - Pad the string so that the length is a multiple of this.
    :param pad_char: char - The character to pad the string with.

    :return: str|bytes - of the padded word.
    """
    if len(pad_char) != 1:
        raise ValueError('pad_char should be a single character')
    return word + pad_char * (n - len(word) % n)


def encrypt(message):
    """
    Encrypt the given message using the hangman cipher so that we can send the
    word back and forth between front end and back end without the user being
    able to see what it is.

    :param message: str - The word to encrypt.

    :return: str - The base64 encoded and encrypted message.
    """
    encoded = base64encode(message.encode('utf-8'))
    padded = pad(encoded, 16, b'=')
    encrypted = cipher.encrypt(padded)
    encrypted_encoded = base64encode(encrypted)
    return encrypted_encoded.decode('ascii')


def decrypt(message):
    """
    Decrypt an encrypted and base64 encoded message to get back the original text
    using the hangman cipher.

    :param message: str - base64 encoded and encrypted message.

    :return: str - The decrypted message.
    """
    encoded = message.encode('ascii')
    decoded = base64decode(encoded)
    decrypted = cipher.decrypt(decoded)
    decoded_decrypted = base64decode(decrypted)
    return decoded_decrypted.decode('utf-8')


def get_hangman_string(word, letters):
    """
    Get a hangman string for a word and letters that the user has already
    chosen. A hangman string is the original word with any letters that do
    not appear in ``letters`` replaced with ``HIDDEN_CHAR``.

    :param word: str - Word for this game.
    :param letters: str - The letters already chosen by the player.

    :return: str - The generated hangman string.
    """
    upper_word = word.upper()
    upper_letters = letters.upper()
    return ''.join(x if x in upper_letters else config.HIDDEN_CHAR for x in upper_word)


def has_won(word, letters):
    if word:
        upper_word = word.upper()
        upper_letters = letters.upper()
        missing_letters = set(upper_word) - set(upper_letters)
        return missing_letters == set()
    else:
        return False


def has_lost(word, letters):
    if word:
        upper_word = word.upper()
        upper_letters = letters.upper()
        incorrect_letters = set(upper_letters) - set(upper_word)
        return len(incorrect_letters) >= config.MAX_INCORRECT_GUESSES
    else:
        return False
