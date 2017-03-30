import string

WORDS_POOL = '3dhubs', 'marvin', 'print', 'filament', 'order', 'layer'
VALID_CHARS = string.ascii_uppercase + string.digits
MAX_INCORRECT_GUESSES = lambda: 5
WON_TEXT = 'Congratulations, you guessed correctly!'
LOST_TEXT = 'Too bad, you ran out of lives!'
PLAYING_TEXT = 'Pick a letter'
HIDDEN_CHAR = '_'
