require('chosen-js')

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

            for (let i = params.chosen.results_data.length - 1; i >= 0; i--) {
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

navigator.geolocation.getCurrentPosition(function (position) {
    let latitude = position.coords.latitude
    let longitude = position.coords.longitude
    $.ajax({
        type: "POST",
        url: "/profile/save_location",
        data: {
            lat: latitude,
            long: longitude,
            csrfmiddlewaretoken: window.token
        },
        error: function (first, e) {
            alert(e)
        }
    })
})