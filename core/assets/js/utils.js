require('chosen-js')

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

window.setupTagsSelect = function(element) {
    element = $(element)
    element.chosen({ width: "100%", no_results_text: "No tags with this name", search_contains: true })

    let chosen = element.parent().find(".chosen-container")
    chosen.find(".chosen-search-input").attr("style", "width: 100%;")
    chosen.addClass("form-control")

    element.on("change", function(e, params) {
        let className = 'tag-' + params.selected
        let tagName = element.find("[value=" + params.selected + "]").text()

        chosen.find(".search-choice > span:contains('" + tagName + "')").parent().addClass(className + " badge-secondary tags")

    })
}