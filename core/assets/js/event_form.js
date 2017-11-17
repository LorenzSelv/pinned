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

// Give styling to the tags input
setupTagsSelect(form.find('#id_tags'))

// Create form field for date time pickers
form.find(".date-time-picker").each(function(){
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

    // Append newly genereted element
    destination.append(newInput)
    // Enable datetimepicker
    newInput.find(".flatpickr").flatpickr({
        enableTime: true,
        dateFormat: "m/d/y H:i",
        minDate: "today"
    })
})
