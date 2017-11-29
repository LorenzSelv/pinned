// Enable map-filters dropdown selection
$("#map-filters .dropdown-menu").find(".dropdown-item").click(function() {
    let selText = $(this).text();
    $(this).parents('.input-group').find('#dropdownMenuButton').html(selText + ' <span class="caret"></span>')
});

// Enable map-filters datetimepicker
$("#map-filters").find("#datepicker").find("input").flatpickr()