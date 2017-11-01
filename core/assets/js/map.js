// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.

require('./event_form.js')

module.exports = {
    initMap: function() {
        let map = new google.maps.Map(document.getElementById('map'), {
            center: { lat: -34.397, lng: 150.644 },
            zoom: 15,
            // Remove the Map/Satellite option
            mapTypeControl: false

        })

        function handleLocationError(browserHasGeolocation, infoWindow, pos) {
            infoWindow.setPosition(pos);
            infoWindow.setContent(browserHasGeolocation ?
                'Error: The Geolocation service failed.' :
                'Error: Your browser doesn\'t support geolocation.');
            infoWindow.open(map);
        }

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
                handleLocationError(true, new google.maps.InfoWindow, map.getCenter());
            });

        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, new google.maps.InfoWindow, map.getCenter());
        }

        // Create marker given event data
        function createMarker(name, description, coords) {
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(coords.lat, coords.lng),
                map: map,
                animation: google.maps.Animation.DROP

            })

            var content = "<div class='map-tooltip'><h1>" + name + "</h1><hr><div class='description'>" + description + "</div></div>"

            var info = new google.maps.InfoWindow({
                content: content
            })

            info.addListener('closeclick', function(){
                info.fixed = false
            })

            marker.addListener('click', function(){
                info.fixed = true
                info.open(this.map, marker)
            })

            marker.addListener('mouseover', function() {
                info.open(this.map, marker)
            })

            marker.addListener('mouseout', function() {
                if(!info.fixed){
                    info.fixed = false
                    info.close()
                }
            })

            return marker
        }

        // Call to events api endpoint and draw markers
        $.ajax('api/events/').done(function(events) {
            for (i = 0; i < events.length; i++) {
                var data = events[i]
                createMarker(data.name, data.description, { lat: data.latitude, lng: data.longitude })
            }
        })

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

            showEventForm(marker.getPosition().lat(), marker.getPosition().lng())

            window.currentMarker = marker
            // TODO: Bring up prompt to enter event details and create the event
        });

    }
}