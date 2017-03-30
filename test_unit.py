# 3rd party
from hypothesis import strategies as st, given, example
import pytest
# local
import config
import hangman
import app


st_hangman_characters = st.sampled_from(config.VALID_CHARS)
st_small_integers = st.integers(min_value=1, max_value=32)


@given(st.text(config.VALID_CHARS), st_small_integers, st_hangman_characters)
def test_pad(text, n, pad_char):
    """
    Verify properties of the pad function.

    :param text: The input text for the pad function.
    :param n: Pad the string to multiples of this.
    :param pad_char: The character to pad with.
    """
    padded = hangman.pad(text, n, pad_char)
    # verify the correct padding character was used
    assert not len(text) % n or padded.endswith(pad_char)
    # verify that the string was padded to the correct length
    assert not len(padded) % n


def test_pad_error():
    """
    Verify that the pad function raises an error when an incorrect pad_char
    is supplied.
    """
    with pytest.raises(ValueError):
        hangman.pad('', 0, 'error')


@given(st.text(config.VALID_CHARS))
@example('3dhubs')
@example('marvin')
@example('print')
@example('filament')
@example('order')
@example('layer')
def test_encrypt_decrypt(text):
    """
    Verify that the functions encrypt and decrypt round trip correctly.

    :param text: The input text to encrypt and decrypt for verification.
    """
    assert hangman.decrypt(hangman.encrypt(text)) == text


@given(st.text(config.VALID_CHARS), st.text(config.VALID_CHARS, max_size=6))
def test_hangman(word, letters):
    """
    Verify the properties of the hangman function.

    :param word: The word that should be guessed.
    :param letters: The letters that the user has already chosen.
    """
    output = hangman.get_hangman_string(word, letters)

    # verify that the length of the word didn't change
    assert len(output) == len(word)

    # get the constituent characters of the various strings as sets
    word_set, output_set, letters_set = map(set, (word, output, letters))

    # verify that the chosen letters that appear in the original word also
    # appear in the output word
    assert word_set & output_set == letters_set & output_set

    # verify that any letters from the original word that do not appear in the
    # chosen letters also do not appear in the output word
    assert word_set - letters_set & output_set == set()


@given(st.text(config.VALID_CHARS, min_size=1),
       st.text(config.VALID_CHARS, max_size=6))
def test_encode_decode_secret_token(word, letters):
    """
    Verify that the encoding / decoding of the secret token round trips correctly.

    :param word: The word to be guessed.
    :param letters: The letters that have been chosen.
    """
    secret_token = app.encode_secret_token(word, letters)
    decoded_word, decoded_letters = app.decode_secret_token(secret_token)
    assert decoded_word == word
    assert decoded_letters == letters


def test_has_won():
    """
    Verify that has_won correctly calculates whether a game is lost or not
    based on the word and the letters chosen.
    """
    # TODO : upper / lower test
    assert not hangman.has_won('abc', 'ab')
    assert not hangman.has_won('abc', 'ab123')
    assert hangman.has_won('abc', 'abc')
    assert hangman.has_won('abc', 'abc123')


def test_has_lost():
    """
    Verify that has_lost correctly calculates whether a game is lost or not
    based on the word and the letters chosen.
    """
    # TODO : upper / lower test
    assert not hangman.has_lost('abc', 'abc')
    assert not hangman.has_lost('abc', 'abc12')
    assert not hangman.has_lost('order', 'dfgopr')
    assert hangman.has_lost('abc', '12345')
    assert hangman.has_lost('abc', 'ab12345')
