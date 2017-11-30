// Get number of currently selected tags
let count = $("#interests-select :selected").length;

// Set up interests tag dropdown
let select = $("#interests-select");
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
    let selectedTags = [];

    $("#interests-select :selected").each(function() {
        selectedTags.push($(this).val());
    });

    sendInterestAjax(selectedTags);
}