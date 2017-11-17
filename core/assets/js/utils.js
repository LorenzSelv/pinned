require('chosen-js')

// Enable map-filters dropdown selection
$("#map-filters .dropdown-menu").find(".dropdown-item").click(function() {
    var selText = $(this).text();
    var selColor = $(this).css("background-color")
    if (selText === 'My Interests') {
        window.map.showInterestedEvents()
    } else {
        window.map.showAllEvents()
    }
    $(this).parents('.input-group').find('#dropdownMenuButton').html(selText + ' <span class="caret"></span>').css("background-color", selColor);
});

// Setup tag select styling on element
window.setupTagsSelect = function(element) {

    // Give the appropriate class to a tag element
    function styleTag(value) {
        let className = 'tag-' + value
        let tagName = element.find("[value=" + value + "]").text()
        element.parent().find(".search-choice > span:contains('" + tagName + "')").parent().addClass(className + " badge-secondary tags")
    }

    element = $(element)

    element
        // Called when chosen is activated on the select field, styles already present tags
        .on("chosen:ready", function(e, params) {

            for (var i = params.chosen.results_data.length - 1; i >= 0; i--) {
                let tag = params.chosen.results_data[i]
                if (tag.selected)
                    styleTag(tag.value)
            }
        })
        // Called when tags get changed, styles newly added tags
        .on("change", function(e, params) {
            if (params.selected)
                styleTag(params.selected)
        })

    // Enable chosen js on the select input field
    element.chosen({ width: "100%", no_results_text: "No tags with this name", search_contains: true })

    // Give styling to container
    let chosen = element.parent().find(".chosen-container")
    chosen.find(".chosen-search-input").attr("style", "width: 100%;")
    chosen.addClass("form-control")

}