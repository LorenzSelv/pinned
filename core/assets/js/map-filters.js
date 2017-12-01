// Contains the options for selecting events
let eventsOptions = {}

// Enable map-filters datetimepicker
$("#map-filters").find("#datepicker").find("input").flatpickr({
    minDate: "today",
    dateFormat: "m/d/y"
})


$("#map-filters").find(".input-group-addon").click(function(){
    $(this).siblings().focus()
})

// Enable map-filters dropdown selection
$("#map-filters").find("#filter-dropdown").find(".dropdown-item").click(function() {
    let selText = $(this).text()
    let selColor = $(this).css("background-color")
    if (selText === 'My Interests') {
        eventsOptions.scope = 'interests'
    } else if (selText === 'All Events') {
        eventsOptions.scope = 'all'
    } else {
        eventsOptions.scope = undefined
        eventsOptions.tag = selText
    }
    if(eventsOptions.scope)
        eventsOptions.tag = undefined
    
    window.map.showEvents(eventsOptions)
    $(this).parents('.input-group').find('#dropdownMenuButton').html(selText + ' <span class="caret"></span>').css("background-color", selColor)
})

// Enable map-filters name search
$("#map-filters").find("#filter-search").on('input', function() {
    eventsOptions.name = $(this).val() !== '' ? $(this).val() : undefined
    window.map.showEvents(eventsOptions)
})

// Enable map-filters date search
$("#map-filters").find("#filter-date").on('change', function() {
    eventsOptions.date = $(this).val() !== '' ? $(this).val() : undefined
    window.map.showEvents(eventsOptions)
})