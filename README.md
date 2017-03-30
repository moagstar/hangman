# Hangman

A simple hangman game built using flask.

## Requirements

The requirements are:

 - chooses a random word out of 6 words: (3dhubs, marvin, print, filament, order, layer)
 - prints the spaces for the letters of the word (eg: ​_ _ _​ _ _ for order)
 - the user can try to ask for a letter and that should be shown on the puzzle (eg: asks for "r" and now it shows ​_ r _​ _ r for order)
 - the user can only ask 5 letters that don't exist in the word and then it's game over
 - if the user wins, congratulate him!

With the following clarifications:

 - the input words also contain numbers, we can assume that only english alphabet + numbers 0 to 9 are supported.
 - underscores should be printed for missing letters in the word.
 - it is ok to use styling if you want, although this is not necessary.

## Implementation

This implementation follows two design principles:

    1. Reduce the amount of state in the backend. By keeping the server state
       to a minimum we can easily test the implementation, and also provide an
       easily scalable implementation.

    2. Ensure that the user cannot just open developer tools and see
       what the word is they should guess. By keeping the implementation stateless
       we need to pass the word to and from backend / frontend. This prevents
       a challenge for hiding the word from the user. We can use AES two way
       encryption to ensure that the user cannot just open developer tools to
       see what the word is that should be guessed.

## Set up

```bash
$ pip install -r requirements.txt -r test-requirements.txt
```

## Testing

The backend is tested using py.test and hypothesis for the most part (with a couple of example
based tests). There is also an integration test for testing the backend and front end
together using the state based testing functionality of hypothesis.

To run the tests:

```bash
$ py.test
```
