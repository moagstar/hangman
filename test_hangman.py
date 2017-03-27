# std
import string
# 3rd party
from hypothesis import strategies as st, given, example
import pytest
# local
import hangman


st_printable_characters = st.sampled_from(string.printable)
st_small_integers = st.integers(min_value=1, max_value=32)


@given(st.text(), st_small_integers, st_printable_characters)
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


@given(st.text())
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


valid_characters = [x for x in string.printable if x != '_']


@given(st.text(valid_characters), st.text(valid_characters, max_size=6))
def test_hangman(word, letters):
    """
    Verify the properties of the hangman function.

    :param word: The word that should be guessed.
    :param letters: The letters that the user has already chosen.
    """
    encrypted = hangman.encrypt(word)
    output = hangman.hangman(encrypted, letters)

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
