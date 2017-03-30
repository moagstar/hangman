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
    var cls = (isCorrect ? 'in' : '') + 'correct';
    $('#_' + letter).addClass(cls).prop("disabled",true).blur();
    var letterElement = window.document.getElementById('_' + letter);
    forceRedraw(letterElement);
}

/**
 * Disable all letters so that no further input can occur, this happens when
 * the game is either won or lost.
 */
function disableAllLetters() {
    $('.letter').prop("disabled",true);
}

/**
 * Show the title which relates to the given id, hiding the playing title. This
 * function is used when the game is won or lost.
 * @param id
 */
function showTitle(id) {
    $('#playing').addClass('hidden');
    $('#' + id).removeClass('hidden');
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
    secretToken = data.secret_token;
    if (data.status == 'lost') {
        disableAllLetters();
        showTitle('lost');
    }
    else if (data.status == 'won') {
        disableAllLetters();
        showTitle('won');
    }
}

/**
 * Callback for handling a user click on a letter.
 * @param letter {string} The letter that was clicked.
 */
function onLetterChosen(letter) {
    var params = {'secret_token': secretToken, 'letter': letter};
    var callback = onHangmanString.bind(null, letter);
    $.getJSON('hangman', params, callback);
}