// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(".events-table").find(".btn-join").on("click", function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            // if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", window.token);
            // }
        }
    })
    let id = $(this).parents("tr").find(".event-id").text()[0]
    $.ajax({
        type: "POST",
        url: id + '/join',
        data: {
            user_id: 1,
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
})