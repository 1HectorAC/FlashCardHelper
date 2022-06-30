var index = 0;
var cardsSize = 0;
var questionSide = true;
var flashCards = [];

// Setup up some cards variables and view of card realated items in html.
function startCardView(cards) {
    flashCards = cards
    cardsSize = flashCards.length;

    // Shuffle cards check.
    if ($('#shuffleCheck').prop('checked'))
        flashCards = shuffleArray(flashCards);

    // Flip questions with answers.
    if ($('#flipCheck').prop('checked'))
        flashCards = flipQuestionsAndAnswers(flashCards);

    //Edit some text.
    $('#index').text(1);
    $('#total').text(cardsSize);
    $('#problemLabel').text("Question");
    $('#problemText').text(flashCards[index].question);

    // Enable next next button if there is more than one card in the flashCards.
    if (flashCards.length > 1)
        $('#nextButton').prop('disabled', false)

    generateNumbers(cardsSize);

    // Setup display if cards.
    $('#introCard').hide();
    $('#displayCard').show();
    $('#nextButton').show();
    $('#previousButton').show();
}

//Sets up change of diplayed question or answer text in html.
function cardFlip() {
    questionSide = !questionSide;
    if (questionSide) {
        $('#problemLabel').text("Question");
        $('#problemText').text(flashCards[index].question);
    }
    else {
        $('#problemLabel').text("Answer");
        $('#problemText').text(flashCards[index].answer);
    }
}

// Show next card in html.
function nextCard() {
    questionSide = true;
    index = ++index;
    // Disable next button if index reaches end of cardsSize.
    if (index + 1 >= cardsSize)
        $('#nextButton').prop('disabled', true)
    // Enable previous button if we move after first card.
    if (index == 1)
        $('#previousButton').prop('disabled', false)
    // Update text to show question.
    if (index <= cardsSize) {
        $('#index').text(index + 1);
        $('#problemLabel').text("Question");
        $('#problemText').text(flashCards[index].question);
    }
}

// Show previous card in html.
function previousCard() {
    questionSide = true;
    index = --index;
    // Disable previous button if index reaches 0.
    if (index == 0)
        $('#previousButton').prop('disabled', true)
    // Enable next button if we move away from final card.
    if (index == cardsSize - 2)
        $('#nextButton').prop('disabled', false)
    // Update text to show question.
    if (index <= cardsSize) {
        $('#index').text(index + 1);
        $('#problemLabel').text("Question");
        $('#problemText').text(flashCards[index].question);
    }
}

//Create buttons with just numbers.
function generateNumbers(num){
    for(let i = 0; i < num; i++){
        $('#numberButtons').append('<button class="btn brownButton" onclick="numberButton('+i+')" style="display:inline; margin: 5px">'+(i+1)+'</button>')
    }
}

// Change view of card based on button.
function numberButton(num){
    // Out of bounds check.
    if(num >= cardsSize || num < 0)
        return;

    // Set variables.
    index = num;
    $('#problemLabel').text("Question");
    $('#problemText').text(flashCards[index].question);
    $('#index').text(index + 1);

    // Disable or Enable the next/previous button depending on index location.
    if(index == cardsSize -1){
        $('#nextButton').prop('disabled', true)
        $('#previousButton').prop('disabled', false)
    }
    else if(index == 0){
        $('#previousButton').prop('disabled', true)
        $('#nextButton').prop('disabled', false)
    }
    else{
        $('#nextButton').prop('disabled', false)
        $('#previousButton').prop('disabled', false)
    }
}

// shuffle array funciton.
function shuffleArray(array) {
    let curId = array.length;
    // There remain elements to shuffle
    while (0 !== curId) {
        // Pick a remaining element
        let randId = Math.floor(Math.random() * curId);
        curId -= 1;
        // Swap it with the current element.
        let tmp = array[curId];
        array[curId] = array[randId];
        array[randId] = tmp;
    }
    return array;
}

// flip answers and questions in array.
function flipQuestionsAndAnswers(array) {
    for (let i = 0; i < array.length; i++) {
        temp = array[i].question;
        array[i].question = array[i].answer;
        array[i].answer = temp;
    }
    return array;
}