// Enable tooltips
$(function() {
    $('[data-toggle="tooltip"]').tooltip()
})

// Enable map-filters dropdown selection
$("#map-filters .dropdown-menu").find(".dropdown-item").click(function() {
    var selText = $(this).text();
    var selColor = $(this).css("background-color")
    $(this).parents('.input-group').find('#dropdownMenuButton').html(selText + ' <span class="caret"></span>').css("background-color", selColor);
});

// Add style to event-form fields
$("#event-form").find("input").addClass("form-control")