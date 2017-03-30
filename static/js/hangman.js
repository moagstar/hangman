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
function updateCharacter(character, isCorrect) {
    var cls = (isCorrect ? 'in' : '') + 'correct';
    $('#_' + character).addClass(cls).prop("disabled",true).blur();
    var characterElement = window.document.getElementById('_' + character);
    forceRedraw(characterElement);
}

/**
 * Disable all characters so that no further input can occur, this happens when
 * the game is either won or lost.
 */
function disableAllCharacters() {
    $('.character').prop("disabled", true);
}

/**
 * Enable all characters buttons.
 */
function enableAllCharacters() {
    $('.character').prop("disabled", false).removeClass("correct incorrect");
}

/**
 * Show the title which relates to the given id, hiding the playing title. This
 * function is used when the game is won or lost.
 * @param id
 */
function showTitle(id) {
    $('.title').addClass('hidden');
    $('#' + id).removeClass('hidden');
}

/**
 * Callback for processing the response from guessing a character.
 * @param character {string} The character that was guessed.
 * @param data {Object} The response from the server.
 */
function onHangmanString(character, data) {

    if (character != '') {
        var isCorrect = data.hangman_string.indexOf(character) < 0;
        updateCharacter(character, isCorrect);
    }

    $("#hangman-string").html(data.hangman_string);
    $("#hangman-image").attr("src", "/static/img/" + data.hangman_image + ".png");

    secretToken = data.secret_token;

    if (data.status == 'lost') {
        disableAllCharacters();
        showTitle('lost');
    }
    else if (data.status == 'won') {
        disableAllCharacters();
        showTitle('won');
    }
    else if (data.status == 'new') {
        enableAllCharacters();
        showTitle('playing');
    }
}

/**
 * Callback for handling a user click on a character.
 * @param character {string} The character that was clicked.
 */
function onCharacterClicked(character) {
    var params = {'secret_token': secretToken, 'character': character};
    var callback = onHangmanString.bind(null, character);
    $.getJSON('hangman', params, callback);
}

/**
 * Callback for handling a user click on the New Word button.
 */
function onNewWordClicked() {
    var callback = onHangmanString.bind(null, '');
    $.getJSON('new_word', {}, callback);
}