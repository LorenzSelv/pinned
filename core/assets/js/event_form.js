require('chosen-js')

let form = $("#event-form")

// Allow canceling out of the form

hideEventForm = function() {
    $("#event-form")[0].reset()
    $("#event-input").addClass("invisible")

    window.currentMarker.setMap(null)
    window.currentMarker = null

    // Find a better way instead of removing the handler, for example
    // a generic key handler in which keys can be registered and unregistered
    $(document).off('keydown') 
}

showEventForm = function(lat, lng){
    $("#event-input").removeClass("invisible")
    $("#event-form #id_latitude").val(lat.toFixed(8))
    $("#event-form #id_longitude").val(lng.toFixed(8))
    $(document).keydown(function(e){
        if(e.keyCode == 27){ // Esc key
            hideEventForm()
        } 
    })
}

$("#event-input").click(hideEventForm)

form.click(function(e){
    e.stopPropagation()
})

form.find(".btn-cancel").click(hideEventForm)

// Add style to event-form fields
form.find("input").addClass("form-control")
form.find("textarea").addClass("form-control")

form.find("#id_tags").attr("data-placeholder", "Select tags for the event").chosen({width: "100%", no_results_text: "No tags with this name", search_contains: true})
// form.find("#id_event_owner").chosen({width: "100%"}) // No need to make it fancier, will be removed as soon as we intruduce login

let chosen = form.find(".chosen-container")
chosen.find(".chosen-search-input").attr("style", "width: 100%;")
chosen.addClass("form-control")
chosen.find(".chosen-")

// Create form field for date time pickers
form.find(".date-time-picker").each(function(){
    let destination = $(this).parents("form").find(".date-times")

    let text = `<div class='col'>
                    <div class='input-group date'>
                        <span class="input-group-addon">
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

    // Append newly genereted element
    destination.append(newInput)

    // Enable datetimepicker
    $(this).flatpickr({
        enableTime: true,
        dateFormat: "m/d/y H:i"
    })
})
