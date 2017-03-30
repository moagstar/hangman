# std
import os
# compatibility
import mock
import contextlib2 as contextlib
# 3rd party
from hypothesis.stateful import RuleBasedStateMachine, rule, precondition
from hypothesis import strategies as st, assume, settings
import capybara
from capybara.dsl import page
# local
import app
import hangman
from config import VALID_CHARS, WON_TEXT, LOST_TEXT, PLAYING_TEXT


# setup capybara / selenium
capybara.app = app.app
os.environ["PATH"] = os.path.dirname(__file__) + os.pathsep + os.environ["PATH"]


# setup mocks
get_word_patcher = mock.patch('app.get_word')
max_incorrect_guesses_patcher = mock.patch('config.MAX_INCORRECT_GUESSES', 2)


class HangmanMachine(RuleBasedStateMachine):
    """

    """
    @property
    def hangman_string(self):
        all_letters = self.correct_letters + self.incorrect_letters
        return hangman.get_hangman_string(self.word, all_letters)

    def __init__(self):
        super(HangmanMachine, self).__init__()
        self.correct_letters, self.incorrect_letters = '', ''
        self.word = None

    @precondition(lambda self: self.word is None)
    @rule(word=st.text(VALID_CHARS, min_size=2, max_size=4))
    def new_game(self, word):
        get_word = get_word_patcher.start()
        max_incorrect_guesses = max_incorrect_guesses_patcher.start()
        get_word.return_value, self.word = word, word
        page.visit("/")

    def _guess_letter_precondition(self, letter, letters):
        assume(not hangman.has_lost(self.word, self.incorrect_letters))
        assume(not hangman.has_won(self.word, self.correct_letters))
        assume(letter not in letters)

    @precondition(lambda self: self.word)
    @rule(random=st.randoms())
    def guess_correct_letter(self, random):
        letter = random.choice(self.word)
        self._guess_letter_precondition(letter, self.correct_letters)
        self.correct_letters += letter
        page.click_button(letter)

    @precondition(lambda self: self.word)
    @rule(letter=st.sampled_from(VALID_CHARS))
    def guess_incorrect_letter(self, letter):
        self._guess_letter_precondition(letter, self.incorrect_letters)
        assume(letter not in self.word)
        self.incorrect_letters += letter
        page.click_button(letter)

    def _verify_hangman_string(self):
        # verify that the hangman string is correctly displayed
        if self.word is not None:
            assert page.find("#hangman-string").text == self.hangman_string

    def _verify_letters(self, letters, cls):
        # verify that all correct_letters have the appropriate class applied
        for letter in letters:
            assert page.find('#_' + letter + '.' + cls).text == letter

    def _verify_hangman_image(self):
        pass # TODO

    def _verify_title_text(self):
        if hangman.has_lost(self.word, self.incorrect_letters):
            assert page.has_text(LOST_TEXT)
        elif hangman.has_won(self.word, self.correct_letters):
            assert page.has_text(WON_TEXT)
        elif self.word:
            assert page.has_text(PLAYING_TEXT)

    def check_invariants(self):
        self._verify_hangman_string()
        self._verify_letters(self.correct_letters, 'correct')
        self._verify_letters(self.incorrect_letters, 'incorrect')
        self._verify_title_text()
        self._verify_hangman_image()

    def teardown(self):
        with contextlib.suppress(RuntimeError):
            get_word_patcher.stop()
        with contextlib.suppress(RuntimeError):
            max_incorrect_guesses_patcher.stop()


with settings(timeout=15):
    HangmanTestCase = HangmanMachine.TestCase
