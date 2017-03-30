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
    RuleBasedStateMachine for performing an integration test of the whole game.
    There are three operations defined:

        ``new_game``        - selects a new word to play.
        ``guess_correct``   - guess a letter which we know to be correct.
        ``guess_incorrect`` - guess a letter which we know to be incorrect.

    The game is modelled as two strings, one for the list of correctly chosen
    letters and one for the incorrectly chosen letters.

    We check the following invariants hold, regardless of which operations are
    performed and in which order, comparing the result from our model with the
    actual game instance:

        ``hangman string``  - verify that the hangman string is displayed and is
                              correct according to our model.

        ``letters``         - verify that the letters in the user interface have
                              a css class applied so that the incorrect /
                              correct difference can be visually shown, checking
                              the values in the actual game against the model.

        ``title text``      - verify that the title text is correct based on
                              whether the model shows that the game is won /
                              lost, or still in progress.

        ``image``           - verify that the image is correctly shown based on
                              the number of correct guesses our model shows.
    """
    @property
    def hangman_string(self):
        """
        Convert the model into an expected hangman string.
        """
        all_letters = self.correct_letters + self.incorrect_letters
        return hangman.get_hangman_string(self.word, all_letters)

    def __init__(self):
        super(HangmanMachine, self).__init__()
        self.correct_letters, self.incorrect_letters = '', ''
        self.word = None

    @precondition(lambda self: self.word is None)
    @rule(word=st.text(VALID_CHARS, min_size=2, max_size=4))
    def new_game(self, word):
        """
        Operation to start a new game, underlying backend is patched to use
        the word which hypothesis selected for us.

        :param word: The word which will be used in this game.
        """
        max_incorrect_guesses_patcher.start()
        get_word = get_word_patcher.start()
        get_word.return_value, self.word = word, word
        page.visit("/")

    def _guess_letter_precondition(self, letter):
        """
        Common preconditions for selecting a letter in the actual game used for
        both incorrect and correct letter guesses.

        We need to prevent a letter being chosen which has been disabled in the
        front end, so we ensure that a letter is not chosen in if the game is
        over, or if the particular letter has already been chosen.

        :param letter: The letter selected by hypothesis.
        """
        assume(not hangman.has_lost(self.word, self.incorrect_letters))
        assume(not hangman.has_won(self.word, self.correct_letters))
        letters = set(self.correct_letters) | set(self.incorrect_letters)
        assume(letter not in letters)

    @precondition(lambda self: self.word)
    @rule(random=st.randoms())
    def guess_correct_letter(self, random):
        """
        Operation to guess a letter correctly.

        :param random: Hypothesis generated random module which can be used to
                       choose a correct letter from the input string.
        """
        letter = random.choice(self.word)
        self._guess_letter_precondition(letter)
        self.correct_letters += letter
        page.click_button(letter)

    @precondition(lambda self: self.word)
    @rule(letter=st.sampled_from(VALID_CHARS))
    def guess_incorrect_letter(self, letter):
        """
        Operation to guess a letter incorrectly.

        :param letter: The letter to guess, filtered in this function using
                       ``assume``.
        """
        self._guess_letter_precondition(letter)
        assume(letter not in self.word)  # ensure incorrect
        self.incorrect_letters += letter
        page.click_button(letter)

    def _verify_hangman_string(self):
        """
        Verify that the hangman string is correctly displayed
        """
        if self.word is not None:
            assert page.find("#hangman-string").text == self.hangman_string

    def _verify_letters(self, letters, cls):
        """
        Verify that all letters in the front end have the appropriate class
        applied, so that a visual distinction between correct / incorrect can
        be made.

        :param letters:
        :param cls:
        """
        for letter in letters:
            assert page.find('#_' + letter + '.' + cls).text == letter

    def _verify_hangman_image(self):
        """
        Verify that the expected image is shown based on the incorrect letters
        in the model.
        """
        pass # TODO

    def _verify_title_text(self):
        """
        Verify that the expected title text is shown based on whether our model
        tells us the game is won, lost or still being played.
        """
        if hangman.has_lost(self.word, self.incorrect_letters):
            assert page.has_text(LOST_TEXT)
        elif hangman.has_won(self.word, self.correct_letters):
            assert page.has_text(WON_TEXT)
        elif self.word:
            assert page.has_text(PLAYING_TEXT)

    def check_invariants(self):
        """
        Check the invariants of the system.
        """
        self._verify_hangman_string()
        self._verify_letters(self.correct_letters, 'correct')
        self._verify_letters(self.incorrect_letters, 'incorrect')
        self._verify_title_text()
        self._verify_hangman_image()

    def teardown(self):
        """
        Undo the mock patches set up for this test.
        """
        with contextlib.suppress(RuntimeError):  # may not be patched
            get_word_patcher.stop()
        with contextlib.suppress(RuntimeError):
            max_incorrect_guesses_patcher.stop()


# run the state machine tests
with settings(timeout=15):
    HangmanTestCase = HangmanMachine.TestCase
