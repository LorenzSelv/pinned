// Send ajax request for leaving event, calls successHandler on success and failureHandler on failure
function sendEventAjax(eventId, action, successHandler, failureHandler){
    $.ajax({
        type: "POST",
        url: eventId + action,
        data: {
            csrfmiddlewaretoken: window.token
        },
        success: successHandler,
        error: failureHandler
    })
}

function joinSuccessHandler(data) {
    data = JSON.parse(data)
}

function leaveSuccessHandler(data){
    data = JSON.parse(data)

}

function failureHandler(firstArgument, error){
    console.log(error)
}


function getEventId(element){
    let id = $(element).parents(".event").find(".event-id").text()

    return id ? id + '/' : ''
}

$(".btn-join").on("click", function() {

    sendEventAjax(getEventId($(this)), 'join', joinSuccessHandler, failureHandler)
})

$(".btn-leave").on("click", function(){
    sendEventAjax(getEventId($(this)), 'leave', leaveSuccessHandler, failureHandler)
})