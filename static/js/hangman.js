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
 * guessed character.
 * @param character {string} The character that was guessed.
 * @param isCorrect {boolean} true if the character appears in the secret word, otherwise false.
 */
function updateLetter(character, isCorrect) {
    var cls = (isCorrect ? 'in' : '') + 'correct';
    $('#_' + character).addClass(cls).prop("disabled",true).blur();
    var characterElement = window.document.getElementById('_' + character);
    forceRedraw(characterElement);
}

/**
 * Disable all characters so that no further input can occur, this happens when
 * the game is either won or lost.
 */
function disableAllLetters() {
    $('.character').prop("disabled",true);
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
 * Callback for processing the response from guessing a character.
 * @param character {string} The character that was guessed.
 * @param data {Object} The response from the server.
 */
function onHangmanString(character, data) {

    var isCorrect = data.hangman_string.indexOf(character) < 0;
    updateLetter(character, isCorrect);

    $("#hangman-string").html(data.hangman_string);
    $("#hangman-image").attr("src", "/static/img/" + data.hangman_image + ".png");

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
 * Callback for handling a user click on a character.
 * @param character {string} The character that was clicked.
 */
function onLetterChosen(character) {
    var params = {'secret_token': secretToken, 'character': character};
    var callback = onHangmanString.bind(null, character);
    $.getJSON('hangman', params, callback);
}