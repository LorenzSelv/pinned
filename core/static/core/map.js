
// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
var map, infoWindow;

function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 15,
        // Remove the Map/Satellite option
        mapTypeControl: false

    });

    infoWindow = new google.maps.InfoWindow;

    //Google's drawing manager (Marker and Hand tools)
    var drawingManager = new google.maps.drawing.DrawingManager({
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_LEFT,
            //Only need a marker from the tools, hand is default
            drawingModes: ['marker'],
            draggable: true
        },
        //Marker should be draggable
        markerOptions: { draggable: true }
    });
    drawingManager.setMap(map);
    // Change the text that appears when hovering over the hand or marker
    $(map.getDiv()).one('mouseover', 'img[src="https://maps.gstatic.com/mapfiles/drawing.png"]', function(e) {
        $(e.delegateTarget).find('img[src="https://maps.gstatic.com/mapfiles/drawing.png"]').each(function() {
            $(this).closest('div[title]').attr('title', function() {
                switch (this.title) {
                    case 'Add a marker':
                        return 'Add me to the map and create an event!';
                        break;
                    case 'Stop drawing':
                        return '';
                        break;
                    default:
                        return this.title;
                }
            });
        });
    });
    // Function called when marker is placed
    google.maps.event.addListener(drawingManager, 'markercomplete', function(marker) {
        // Just printing out the marker's location
        console.log(marker.getPosition().lat());
        console.log(marker.getPosition().lng());
        // Select the 'hand' tool
        drawingManager.set('drawingMode');
        $("#event-form").removeClass("hidden")
        $("#event-form #id_latitude").val(marker.getPosition().lat())
        $("#event-form #id_longitude").val(marker.getPosition().lng())
        $("#event-form #id_user").val(1)
        // TODO: Bring up prompt to enter event details and create the event
    });

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {

            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(pos.lat, pos.lng),
                map: map,
                animation: google.maps.Animation.DROP,
                label: 'Pinned HQ.'
            });

            map.setCenter(pos);

        }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
        });

    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }

    function createTemporaryMarker(coords) {
        var marker = new google.maps.Marker({
            position: coords,
            map: map,
            animation: google.maps.Animation.DROP
        })
        return marker
    }

    // google.maps.event.addListener(map, 'click', function(event){
    //   if(!window.temp)
    //     window.temp = createTemporaryMarker(event.latLng)
    // })

}

function add_pin(map, lt, lg) {
    var pos = { lat: lt, lng: lg };
    var marker = new google.maps.Marker({
        position: pos,
        map: map
    });
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}