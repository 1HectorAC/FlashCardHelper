var index = 0;
var cardsSize = 0;
var questionSide = true;
var flashCards = [];

// Sets the flash card variable and related variable.
function setFlashCards(cards){

    flashCards = cards;
    cardsSize = cards.length;
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
    console.log(index)
    // Disable next button if index reaches end of cardsSize.
    if(index +1 >= cardsSize){
        console.log("disable next button");
        $('#nextButton').prop('disabled', true)
    }
    // Enable previous button if we move after first card.
    if(index == 1){
        console.log("enable previous button")
        $('#previousButton').prop('disabled', false)
    }
    // Update text to show question.
    if(index <= cardsSize){
        $('#problemLabel').text("Question");
        $('#problemText').text(flashCards[index].question);
    }
}

// Show previous card in html.
function previousCard(){
    questionSide = true;
    index = --index;
    console.log(index)
    // Disable previous button if index reaches 0.
    if(index == 0){
        console.log("disable next button");
        $('#previousButton').prop('disabled', true)
    }
    // Enable next button if we move away from final card.
    if(index == cardsSize - 2){
        console.log("enable previous button")
        $('#nextButton').prop('disabled', false)
    }
    // Update text to show question.
    if(index <= cardsSize){
        $('#problemLabel').text("Question");
        $('#problemText').text(flashCards[index].question);
    }
}