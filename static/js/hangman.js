var letters = '';

/**
 * Force an element to redraw itself.
 * @param element {HTMLElement} The element to redraw.
 */
var forceRedraw = function(element){
    var saved = element.style.display;
    element.style.display = 'none';
    var fudge = element.offsetHeight;
    element.style.display = saved;
};

/**
 * Update the user interface after retrieving the response about a particular
 * guessed letter.
 * @param letter {string} The letter that was guessed.
 * @param isCorrect {boolean} true if the letter appears in the secret word, otherwise false.
 */
function updateLetter(letter, isCorrect) {
    var classes = 'disabled ' + (isCorrect ? 'red' : 'green');
    $('#' + letter).addClass(classes).blur();
    var letterElement = window.document.getElementById(letter);
    forceRedraw(letterElement);
}

/**
 * Callback for processing the response from guessing a letter.
 * @param letter {string} The letter that was guessed.
 * @param data {Object} The response from the server.
 */
function onHangmanString(letter, data) {
    var isCorrect = data.hangman_string.indexOf(letter) < 0;
    updateLetter(letter, isCorrect);
    $("#hangman-string").html(data.hangman_string);
}

/**
 * Callback for handling a user click on a letter.
 * @param secret {string} The encrypted secret word we are guessing.
 * @param letter {string} The letter that was clicked.
 */
function onLetterChosen(secret, letter) {
    if (letters.indexOf(letter) < 0) {
        letters += letter;
        var params = {'secret': secret, 'letters': letters};
        var callback = onHangmanString.bind(null, letter);
        $.getJSON('hangman', params, callback);
    }
}