# std
import base64
# 3rd party
from Crypto.Cipher import AES


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


def encrypt(word):
    """
    Encrypt the given word using the hangman cipher so that we can send the
    word back and forth between front end and back end without the user being
    able to see what it is.

    :param word: str - The word to encrypt.

    :return: str - The base64 encoded and encrypted word.
    """
    encoded = base64.encodebytes(word.encode('utf-8'))
    padded = pad(encoded, 16, b'=')
    encrypted = cipher.encrypt(padded)
    encrypted_encoded = base64.encodebytes(encrypted)
    return encrypted_encoded.decode('ascii')


def decrypt(encrypted_word):
    """
    Decrypt an encrypted and base64 encoded word to get back the original text
    using the hangman cipher.

    :param encrypted_word: str - base64 encoded and encrypted word.

    :return: str - The decrypted word.
    """
    encoded = encrypted_word.encode('ascii')
    decoded = base64.decodebytes(encoded)
    decrypted = cipher.decrypt(decoded)
    decoded_decrypted = base64.decodebytes(decrypted)
    return decoded_decrypted.decode('utf-8')


def hangman(encrypted_word, letters):
    """
    Get a hangman string for an encrypted word and letters that the user has
    already chosen.

    :param encrypted_word: str - Encrypted word for this game.
    :param letters: str - The letters already chosen by the player.

    :return: str - The generated hangman string.
    """
    word = decrypt(encrypted_word)
    return ''.join(x if x in letters else '_' for x in word)
