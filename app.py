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
    :return:
    """
    return random.choice(WORDS_POOL)


def encode_secret_token(word, letters):
    """
    :param word:
    :param letters:
    :return:
    """
    token = ';'.join([word, letters])
    encrypted = token#hangman.encrypt(token)
    return urllib.parse.quote(encrypted, safe='')


def decode_secret_token(secret_token):
    """

    :param secret_token:
    :return:
    """
    secret_token = urllib.parse.unquote(secret_token)
    decrypted = secret_token#hangman.decrypt(secret_token)
    return decrypted.split(';')


@app.route('/')
def index():
    """
    """
    word = get_word()
    return render_template(
        'index.html',
        secret_token=encode_secret_token(word, ''),
        hangman=hangman.get_hangman_string(word, ''),
        letters_to_choose_from=config.VALID_CHARS,
        won=config.WON_TEXT,
        lost=config.LOST_TEXT,
        playing=config.PLAYING_TEXT,
    )


@app.route('/hangman')
def hangman_get():
    """

    :return:
    """
    secret_token = request.args['secret_token']
    word, letters = decode_secret_token(secret_token)
    letters += request.args['letter']

    if hangman.has_lost(word, letters):
        status = 'lost'
    elif hangman.has_won(word, letters):
        secret_token = encode_secret_token(word, letters)
        status = 'won'
    else:
        secret_token = encode_secret_token(word, letters)
        status = 'playing'

    return jsonify(
        hangman_string=hangman.get_hangman_string(word, letters),
        secret_token=secret_token,
        status=status,
    )


if __name__ == '__main__':
    app.run()
