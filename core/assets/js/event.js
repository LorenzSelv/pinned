// Bind join and leave buttons to their handlers
function bindButtons() {
    $(".btn-join").off("click").on("click", function() {
        sendEventAjax(getEventId($(this)), 'join', (data) => { joinSuccessHandler($(this), JSON.parse(data)) }, failureHandler)
    })

    $(".btn-leave").off("click").on("click", function() {
        sendEventAjax(getEventId($(this)), 'leave', (data) => { leaveSuccessHandler($(this), JSON.parse(data)) }, failureHandler)
    })
}

// Send ajax request for leaving event, calls successHandler on success and failureHandler on failure
function sendEventAjax(eventId, action, successHandler, failureHandler) {
    $.ajax({
        type: "POST",
        url: eventId + 'member',
        data: {
            action: action,
            csrfmiddlewaretoken: window.token
        },
        success: successHandler,
        error: failureHandler
    })
}

// Convert each button to its opposite one
function changeButton(element, action) {
    if (action == 'join') {
        $(element).removeClass('btn-join').addClass('btn-leave').text("Leave")
    }

    if (action == 'leave') {
        $(element).removeClass('btn-leave').addClass('btn-join').text("Join")
    }

    // Re-bind listeners to buttons (since their classes have changed)
    bindButtons()
}

// Update the list and amount of participans 
function updateParticipants(element, participants) {
    let tbody = $('.event-participants-list').find('tbody')
    let amtParticipants = $(element).parents('.event').find('.event-participants-amount')

    // Do this only in the event detail page (getEventId returns an empty string)
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

// Handler for succesful join
function joinSuccessHandler(element, data) {
    if (data.result) {
        changeButton(element, 'join')
        updateParticipants(element, data.participants)
    }
}

// Handler for succesful leave 
function leaveSuccessHandler(element, data) {
    if (data.result) {
        changeButton(element, 'leave')
        updateParticipants(element, data.participants)
    }
}

function failureHandler(firstArgument, error) {
    console.log(error)
}


// Get id of the currently selected event
// Note: this function allows to discern between event detail page and events list, since
// if no id is found this means that the current page is the event detail one
function getEventId(element) {
    let id = $(element).parents(".event").find(".event-id").text()

    return id ? id + '/' : ''
}

bindButtons()