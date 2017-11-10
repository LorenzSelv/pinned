require('chosen-js')

window.setupTagsSelect = function(element) {
    element = $(element)
    element.chosen({ width: "100%", no_results_text: "No tags with this name", search_contains: true })

    let chosen = element.parent().find(".chosen-container")
    chosen.find(".chosen-search-input").attr("style", "width: 100%;")
    chosen.addClass("form-control")

    element.on("change", function(e, params) {
        let className = 'tag-' + params.selected
        let tagName = element.find("[value=" + params.selected + "]").text()

        chosen.find(".search-choice > span:contains('" + tagName + "')").parent().addClass(className + " badge-secondary tags-profile")

    })
}