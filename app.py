# std
import string
import random
# compat
import six.moves.urllib as urllib
# 3rd party
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
# local
import hangman


app = Flask(__name__)
Bootstrap(app)


words = '3dhubs', 'marvin', 'print', 'filament', 'order', 'layer'


@app.route('/')
def index():
    """
    """
    secret = hangman.encrypt(random.choice(words))
    return render_template(
        'index.html',
        secret=urllib.parse.quote(secret, safe=''),
        hangman=hangman.hangman(secret, ''),
        letters_to_choose_from=string.ascii_uppercase + string.digits
    )


@app.route('/hangman')
def hangman_get():
    encrypted_word = urllib.parse.unquote(request.args['secret'])
    letters = request.args['letters']
    hangman_string = hangman.hangman(encrypted_word, letters)
    return jsonify(hangman_string=hangman_string)


def run_dev_server():
    app.debug = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()


if __name__ == '__main__':
    run_dev_server()