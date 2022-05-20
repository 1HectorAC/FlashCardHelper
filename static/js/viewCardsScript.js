var index = 0;
var cardsSize = 0;
var questionSide = true;
var flashCards = [];

// Setup up some cards variables and view of card realated items in html.
function startCardView(cards){
    flashCards = cards
    cardsSize = flashCards.length;
    $('#index').text(1);
    $('#total').text(cardsSize);
    $('#problemLabel').text("Question");
    $('#problemText').text(flashCards[index].question);
    // Enable next next button if there is more than one card in the flashCards.
    if(flashCards.length > 1)
        $('#nextButton').prop('disabled', false)  
    // Setup display if cards.
    $('#introCard').hide();
    $('#displayCard').show();
}

//Sets up change of diplayed question or answer text in html.
function cardFlip(){
    questionSide = !questionSide;
    if(questionSide){
        $('#problemLabel').text("Question");
        $('#problemText').text(flashCards[index].question);
    }
    else{
        $('#problemLabel').text("Answer");
        $('#problemText').text(flashCards[index].answer);
    }

}

// Show next card in html.
function nextCard(){
    questionSide = true;
    index = ++index;
    // Disable next button if index reaches end of cardsSize.
    if(index +1 >= cardsSize)
        $('#nextButton').prop('disabled', true)
    // Enable previous button if we move after first card.
    if(index == 1)
        $('#previousButton').prop('disabled', false)
    // Update text to show question.
    if(index <= cardsSize){
        $('#index').text(index + 1);
        $('#problemLabel').text("Question");
        $('#problemText').text(flashCards[index].question);
    }
}

// Show previous card in html.
function previousCard(){
    questionSide = true;
    index = --index;
    // Disable previous button if index reaches 0.
    if(index == 0)
        $('#previousButton').prop('disabled', true)
    // Enable next button if we move away from final card.
    if(index == cardsSize - 2)
        $('#nextButton').prop('disabled', false)
    // Update text to show question.
    if(index <= cardsSize){
        $('#index').text(index + 1);
        $('#problemLabel').text("Question");
        $('#problemText').text(flashCards[index].question);
    }
}