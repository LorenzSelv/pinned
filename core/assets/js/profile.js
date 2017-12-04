// Set up interests tag dropdown
let select = $("#interests-select")

// Setup tag select styling on element
function setupTagsSelect(element) {

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


    // Prevent modifying interests for other users
    let allowEdit = $("#same-user").length ? ($("#same-user").text() == 'True') : false

    if (!allowEdit) {
        let card = $(".card-info.card-interests").find(".card-block")
        let newCard = $("<div></div>").css({
            'width': card.width(),
            'height': card.height(),
            'background-color': 'transparent',
            'position': 'absolute',
            'bottom': 0
        })

        card.parent().append(newCard)
    }

}

setupTagsSelect(select)

// Send tags to view
function sendInterestAjax(selectedTags) {
    $.ajax({
        type: "POST",
        data: {
            selectedTags: selectedTags,
            csrfmiddlewaretoken: window.token
        }
    })
}

// Send request when selected tags are changed
document.getElementById("interests-select").onchange = function() {
    let selectedTags = []

    $("#interests-select :selected").each(function() {
        selectedTags.push($(this).val())
    })

    sendInterestAjax(selectedTags)
}