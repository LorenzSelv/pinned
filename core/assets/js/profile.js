$('#update_modal').on('shown.bs.modal', function () {
  $('#updated-input').trigger('focus');
})

var table = document.getElementById("interests-table");

$("#interests_dropdown").parent().find(".dropdown-item").click(function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", window.token);
        }
    })

	var interest = $(this).text();
	if (!interest){
		return;
	}

    /*
	$.ajax({
        type: "POST",
        url: id + '/join',
        data: {
            user_id: interest,
            csrfmiddlewaretoken: window.token
        },
        success: (data) => {
            data = JSON.parse(data)
            console.log(data)

            if(data.result)
                $(this).css('background-color', 'green')
            else
                $(this).css('background-color', 'red')
        },
        error: function(first, e) {
            alert(e)
        }
    })
    */

	var row = table.insertRow(-1);
	var cell = row.insertCell(-1);
	cell.innerHTML = interest;

    

	return $("#add-interest").val('');
})