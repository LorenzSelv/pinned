var count = $("#interests-select :selected").length;

/* 
 * Get csrf cookie
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// set up interests tag dropdown
let select = $("#interests-select");
setupTagsSelect(select)

/* 
 * Send tags to views
 */
function sendInterestAjax(selectedTags) {
	var csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        data: {
        	selectedTags: selectedTags,
            csrfmiddlewaretoken: csrftoken
        }
    })
}

/* 
 * listen for select-box change
 * if change send post request to update tags
 */
function bindButtons() {
    document.getElementById("interests-select").onchange = function(){
    	var selectedTags = [];  
    	  
    	$("#interests-select :selected").each(function(){
        	selectedTags.push($(this).val()); 
    	});
    	
    	sendInterestAjax(selectedTags);
	}
}

bindButtons();