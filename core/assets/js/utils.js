require('chosen-js')

// Save user's location
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {

        // If the page is not allowed to save location, just return
        if (!window.token)
            return

        // Get coordinates
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
            error: function(first, e) {
                alert(e)
            }
        })
    }, function() { console.log("Unable to obtain coordinates") })

} else {
    console.log("Unable to save user coordinates, geolocation error")
}

require("./notifications.js")