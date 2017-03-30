# std
import random
import sys
# compatibility
import six.moves.urllib as urllib
# 3rd party
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
# local
import config
import hangman
from config import WORDS_POOL


app = Flask(__name__)
Bootstrap(app)


def get_word():
    """
    Retrieve the word which should be used for the game.:
    """
    return random.choice(WORDS_POOL)


def encode_secret_token(word, characters):
    """
    Encode the word for this game and the already selected characters into a
    secret token which can be safely passed to the front end without the
    user seeing what the word to be guessed is.

    The resulting encoded token is encrypted and url quoted for safely
    passing to the front end.

    :param word: The word to be guessed.
    :param characters: The characters already chosen.

    :return: The word and characters encoded, encrypted and url quoted.
    """
    token = ';'.join([word, characters])
    encrypted = hangman.encrypt(token)
    return urllib.parse.quote(encrypted, safe='')


def decode_secret_token(secret_token):
    """
    Decode a secret token that was previously encoded, encrypted and quoted
    to get back the word for the game and the characters that have already been
    chosen.

    :param secret_token: The secret token containing the encoded data.

    :return: tuple of word, characters unquoted, decrypted and decoded from the
             secret token.
    """
    secret_token = urllib.parse.unquote(secret_token)
    decrypted = hangman.decrypt(secret_token)
    return decrypted.split(';')


@app.route('/')
def index():
    """
    Retrieve the rendered index page.
    """
    word = get_word()
    return render_template(
        'index.html',
        secret_token=encode_secret_token(word, ''),
        hangman=hangman.get_hangman_string(word, ''),
        characters_to_choose_from=config.VALID_CHARS,
        won=config.WON_TEXT,
        lost=config.LOST_TEXT,
        playing=config.PLAYING_TEXT,
    )


@app.route('/hangman')
def hangman_get():
    """
    Handle the GET for retrieving the hangman string for a particular word and
    chosen characters.

    The result is the hangman string and the updated secret token.
    """
    secret_token = request.args['secret_token']
    word, characters = decode_secret_token(secret_token)
    characters += request.args['character']

    if hangman.has_lost(word, characters):
        status = 'lost'
    elif hangman.has_won(word, characters):
        secret_token = encode_secret_token(word, characters)
        status = 'won'
    else:
        secret_token = encode_secret_token(word, characters)
        status = 'playing'

    return jsonify(
        hangman_string=hangman.get_hangman_string(word, characters),
        secret_token=secret_token,
        status=status,
    )


if __name__ == '__main__':
    app.run()
