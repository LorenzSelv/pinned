// Send ajax request for joining event, calls successHandler on success and failureHandler on failure
function sendJoinAjax(element, successHandler, failureHandler){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            // if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", window.token);
            // }
        }
    })

    let id = $(element).parents(".event").find(".event-id").text()

    $.ajax({
        type: "POST",
        url: id + '/join',
        data: {
            csrfmiddlewaretoken: window.token
        },
        success: successHandler,
        error: failureHandler
    })
}

// Send ajax request for leaving event, calls successHandler on success and failureHandler on failure
function sendLeaveAjax(element, successHandler, failureHandler){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            // if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", window.token);
            // }
        }
    })

    let id = $(element).parents(".event").find(".event-id").text()

    $.ajax({
        type: "POST",
        url: id + '/leave',
        data: {
            csrfmiddlewaretoken: window.token
        },
        success: successHandler,
        error: failureHandler
    })
}

function joinSuccessHandler(data) {

    data = JSON.parse(data)
    // if(data.result){
    //
    // }else{
    //
    // }

}

function leaveSuccessHandler(data){
    data = JSON.parse(data)

}

function failureHandler(firstArgument, error){
    console.log(error)
}


$(".btn-join").on("click", function() {
    sendJoinAjax($(this), joinSuccessHandler, failureHandler)
})

$(".btn-leave").on("click", function(){
    sendLeaveAjax($(this), leaveSuccessHandler, failureHandler)
})