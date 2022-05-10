//Handle form for signing up.
$("form[name=signup_form]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

//Handle form for login.
$("form[name=login_form]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

// Handle form to add a cards list.
$("form[name=addCards]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/addCards",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

// Handle form to add a card.
$("form[name=addCard]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/user/addCard",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            location.reload();
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

// Make text boxes for entering questions and answer cards.
function GenerateBoxes(){
    $('#numberSection').hide()
    num = $('#questionTotal').val()
    $('#questionSection').append('<p>Total:' + num + '</p>')
    $('#questionSection').append('<p>Question and then Answer</p>')

    for(let i = 0; i < num; i++){
        card = $('<div>')
        questionPart = $('<input type="text" class="questionPart" name="questionPart" required>')
        answerPart = $('<input type="text" class="answerPart" name="answerPart" required>')
        card.append(questionPart)
        card.append(answerPart)
        $('#questionSection').append(card)
    }
    $('#questionSection').append('<input type="submit" value="Enter" class="btn btn-primary"></input>')
    $('#questionSection').show()
}