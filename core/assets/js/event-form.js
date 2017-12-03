let form = $("#event-form")

// Allow closing the form by clicking outside of the modal
hideEventForm = function() {
    $("#event-form")[0].reset()
    $("#event-input").addClass("invisible")

    window.currentMarker.setMap(null)
    window.currentMarker = null

    $(document).off('keydown')
}

// Show event form and initialize hidden fields
showEventForm = function(lat, lng) {
    $("#event-input").removeClass("invisible")
    $("#event-form #id_latitude").val(lat.toFixed(8))
    $("#event-form #id_longitude").val(lng.toFixed(8))
    $(document).keydown(function(e) {
        if (e.keyCode == 27) { // Esc key
            hideEventForm()
        }
    })
}

$("#event-input").click(hideEventForm)

// Prevent form from closing on click
form.click(function(e) {
    e.stopPropagation()
})

form.find(".btn-cancel").click(hideEventForm)

// Add style to event-form fields
form.find("input").addClass("form-control")
form.find("textarea").addClass("form-control")

// Give styling to the tags input
chosenSettings = { width: "100%", no_results_text: "No tags with name", search_contains: true }

tagField = form.find('#id_tag')
tagField.find("option[value='']").text("None")
tagField.chosen(chosenSettings)

// Give styling to container
let chosen = tagField.parent().find(".chosen-container")

function styleChosen() {
    chosen.find(".chosen-search-input").attr("style", "width: 100%;")

    chosen.find(".chosen-results").on("DOMSubtreeModified", function() {
        let drop = $(this).parents(".chosen-drop")
        let noResults = drop.find(".no-results")

        if (noResults.length) {
            let tagName = $(".chosen-search-input").val()
            let span = noResults.find("span")
            let createTag = $(`<span class="create-tag">Create new tag with this name? <i class="fa fa-plus" aria-hidden="true"></i>`)

            if (!drop.find(".create-tag").length) {

                function creationHandler(data) {
                    data = JSON.parse(data)
                    tagField.append($("<option selected value=" + data.id + ">" + tagName + "</option>"))

                    tagField.chosen('destroy')
                    tagField.chosen(chosenSettings)
                    chosen = tagField.parent().find(".chosen-container")
                    styleChosen()
                }

                drop.append(createTag)
                createTag.find(".fa.fa-plus").on("click", function() {
                    
                    $.ajax({
                        type: "POST",
                        url: "/tag/create",
                        data: {
                            tagName: tagName,
                            csrfmiddlewaretoken: window.token
                        },
                        success: creationHandler
                    })
                })
            }
        } else {
            let createTag = drop.find(".create-tag")
            if (createTag.length) {
                createTag.remove()
            }
        }

    })

    chosen.addClass("form-control")
}

styleChosen()

// Create form field for date time pickers
let pickers = []

form.find(".date-time-picker").each(function() {
    $(this).attr("data-input", "")
    let destination = $(this).parents("form").find(".date-times")

    let text = `<div class='col'>
                    <div class='input-group date flatpickr'>
                        <span class="input-group-addon" data-toggle>
                            <span class="fa fa-calendar"></span>
                        </span>
                    </div>
                </div>`

    let pTag = $(this).parents("p")

    let label = pTag.find("label")

    let newInput = $(text)
    newInput.find('.input-group').prepend($(this))
    newInput.prepend(label)

    pTag.remove()

    // Append newly generated element
    destination.append(newInput)
    // Enable and savev datetimepicker
    let element = $(this).is("#id_start_date_time") ? 'start' : 'end'

    let now = new Date()

    pickers[element] = {
        'picker': newInput.find(".flatpickr").flatpickr({
            enableTime: true,
            dateFormat: "m/d/y H:i",
            minDate: now.setTime(now.getTime() + 3600 * 1000),
            wrap: true
        }),
        'element': $(this)
    }
})

// Update minimum date for end picker
pickers.start.element.change(function() {
    let start = new Date(pickers.start.element.val())
    let minEnd = start.setTime(start.getTime() + 15 * 60 * 1000)

    pickers.end.picker.config.minDate = minEnd
    let end = new Date(pickers.end.element.val())
    if (end < minEnd) {
        pickers.end.element.val("")
    }
})

form.submit(function(event) {
    var start = pickers.start.picker
    var end = pickers.end.picker
    if (start.selectedDates == "" || end.selectedDates == "") {
        event.preventDefault()
        alert("Please fill out both date fields!")
    } else if (invalidStartDate(start)) {
        event.preventDefault()
        alert("Start date cannot be before the current time!")
    }
})

function invalidStartDate(start) {
    let currentTime = new Date()
    let selectedTime = new Date(start.selectedDates[0])
    return selectedTime < currentTime
}
