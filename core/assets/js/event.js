// Send ajax request for leaving event, calls successHandler on success and failureHandler on failure
function sendEventAjax(eventId, action, successHandler, failureHandler) {
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

function changeButton(element, action) {
    if (action == 'join') {
        $(element).removeClass('btn-join').addClass('btn-leave').text("Leave")
    }

    if (action == 'leave') {
        $(element).removeClass('btn-leave').addClass('btn-join').text("Join")
    }

    bindButtons()
}

function updateParticipants(element, participants) {
    let tbody = $('.event-participants-list').find('tbody')
    let amtParticipants = $(element).parents('.event').find('.event-participants-amount')

    if (!getEventId(element)) {
        tbody.empty()
        if (!participants.length)
            tbody.append("<tr><td>No participant yet</td></tr>")
        for (let i = participants.length - 1; i >= 0; i--) {
            tbody.append("<tr><td>" + participants[i] + "</td></tr>")
        }

    }

    amtParticipants.text(participants.length)
}

function joinSuccessHandler(element, data) {
    if (data.result) {
        changeButton(element, 'join')
        updateParticipants(element, data.participants)
    }
}

function leaveSuccessHandler(element, data) {
    if (data.result) {
        changeButton(element, 'leave')
        updateParticipants(element, data.participants)
    }
}

function failureHandler(firstArgument, error) {
    console.log(error)
}


function getEventId(element) {
    let id = $(element).parents(".event").find(".event-id").text()

    return id ? id + '/' : ''
}

function bindButtons() {
    $(".btn-join").off("click").on("click", function() {
        sendEventAjax(getEventId($(this)), 'join', (data) => { joinSuccessHandler($(this), JSON.parse(data)) }, failureHandler)
    })

    $(".btn-leave").off("click").on("click", function() {
        sendEventAjax(getEventId($(this)), 'leave', (data) => { leaveSuccessHandler($(this), JSON.parse(data)) }, failureHandler)
    })
}

bindButtons()