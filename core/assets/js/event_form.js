let form = $("#event-form")

// Allow canceling out of the form
form.find(".btn-cancel").on("click", function() {
    $("#event-form")[0].reset()
    $("#event-input").addClass("invisible")

    window.currentMarker.setMap(null)
    window.currentMarker = null
})

// Add style to event-form fields
form.find("input").addClass("form-control")
form.find("textarea").addClass("form-control")


// Create form field for date time pickers
form.find(".date-time-picker").each(function(){
    let text = `<div class='input-group date'>
                    <span class="input-group-addon">
                        <span class="fa fa-calendar"></span>
                    </span>
                </div>`

    let oldInput = $(this).parents("p")
    let newInput = $(text).prepend($(this))

    // Append newly genereted element
    oldInput.append(newInput)

    // Enable datetimepicker
    $(this).flatpickr({
        enableTime: true,
        dateFormat: "m/d/y H:i"
    })
})
