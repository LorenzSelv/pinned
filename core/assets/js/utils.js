// Enable map-filters dropdown selection
$("#map-filters .dropdown-menu").find(".dropdown-item").click(function() {
    var selText = $(this).text();
    var selColor = $(this).css("background-color")
    if (selText === 'My Interests') {
        window.map.showInterestedEvents()
    }
    else {
        window.map.showAllEvents()
    }
    $(this).parents('.input-group').find('#dropdownMenuButton').html(selText + ' <span class="caret"></span>').css("background-color", selColor);
});

// Enable map-filters datetimepicker
$("#map-filters").find("#datepicker").find("input").flatpickr()