//Handle form for signing up.
$("form[name=signup_form]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/dashboard/";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

//Handle form for login.
$("form[name=login_form]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/dashboard/";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

// Handle form to add a cards list.
$("form[name=addCards]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/addCards",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/dashboard/";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

// Handle form to add a card.
$("form[name=addCard]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/user/addCard",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            location.reload();
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

// Handle form to edit a card.
$("form[name=editCard]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/user/editCard",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            location.reload();
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

// Handle form to edit cards set.
$("form[name=editCards]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/user/editCards",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/dashboard/";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});

// Handle form to edit users name.
$("form[name=editName]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/user/editName",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/editUser/";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});

// Handle form to edit users email.
$("form[name=editEmail]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/user/editEmail",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/editUser/";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});

// Handle form to edit users password.
$("form[name=editPassword]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/user/editPassword",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/editUser/";
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});

// Make text boxes for entering questions and answer cards.
function GenerateBoxes() {
    num = $('#questionTotal').val()

    // Length check
    if(num <= 0 || num > 20){
        $('.error2').text('Number must be between 1-20')
        return
    }

    $('#numberSection').hide()

    $('#questionSection').append('<p >Note: Questions or Answers must be 100 characters or less.</p>')
    $('#questionSection').append('<p style="display:inline-block; width:50%">Questions</p>')
    $('#questionSection').append('<p style="display:inline-block; width:50%">Answers</p>')

    for (let i = 0; i < num; i++) {
        card = $('<div class="row">')
        // Setup Question part
        questionPart = $('<div class="col-md-6">')
        questionPart.append('<p style="margin:2px">Q' + (i + 1) + '</p>')
        questionPart.append($('<input type="text" class="questionPart form form-control" name="questionPart" maxlength="100" required>'))

        // Setup Answer part
        answerPart = $('<div class="col-md-6">')
        answerPart.append('<p style="margin:2px">A' + (i + 1) + '</p>')
        answerPart.append($('<input type="text" class="answerPart form form-control" name="answerPart" maxlength="100" required>'))

        card.append(questionPart)
        card.append(answerPart)
        $('#questionSection').append(card)
    }
    $('#questionSection').append('<p class="error error--hidden" style="color:rgb(255, 177, 177)"></p>')
    $('#questionSection').append('<input type="submit" value="Enter" class="btn lPinkButton" style="margin-top:10px"></input>')
    $('#questionSection').show()
}

// Toggle display of a panel.
function toggleEditCard(num) {
    if ($('#cardDropdown' + num).css('display') == 'none')
        $('#cardDropdown' + num).fadeIn('fast');
    else
        $('#cardDropdown' + num + '').fadeOut('fast');
}

// Show confirmation window when deleting a cards List.
function deleteCardsListConfirmation(cardsTitle) {
    if (confirm("Delete flash cards set \""+cardsTitle+"\" Confirmation.") == true)
        window.location.href = "/user/deleteCards/"+ cardsTitle; 
}

// Show confirmation window when deleting a card.
function deleteCardConfirmation(cardsTitle, index, question, answer) {
    if (confirm("Delete card Confirmation.\n Question: "+question+"\n Answer: "+answer) == true)
        window.location.href = "/user/deleteCard/"+cardsTitle+"/"+ index; 
}