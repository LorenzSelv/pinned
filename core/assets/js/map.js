// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.

require('./event_form.js')

let map;
let markers = [];

function sendEventsAjax(scope, tag) {
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/events/api/",
        data: {
            scope: scope
        },
        success: (events) => {
            //Create markers on the map depending on the events returned
            for (i = 0; i < events.length; i++) {
                //TODO: Maybe find better way of accessing tag name
                if (tag === null || events[i].tag_code.indexOf(tag) !== -1) {
                    let data = events[i]
                    window.map.createMarker(data.name,
                        data.description, data.id, data.tag_code, {
                        lat: data.latitude,
                        lng: data.longitude
                    })
                }
            }
        },
        error: function(first, e) {
            alert(e)
        }
    })
}

module.exports = {
    initMap: function() {
        map = new google.maps.Map(document.getElementById('map'), {
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

        window.map.showAllEvents()

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
            drawingManager.set('drawingMode');

            // TODO: pass the current logged in user to the EventForm
            showEventForm(marker.getPosition().lat(), marker.getPosition().lng())

            window.currentMarker = marker
            // TODO: Bring up prompt to enter event details and create the event
        });
    },

    // Create marker given event data
    createMarker: function(name, description, id, tag, coords) {
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(coords.lat, coords.lng),
            map: map,
            animation: google.maps.Animation.DROP
        })

        var content = "<h1><div class='event-info'><a href='/events/" + id + "'>" + name + "</a></h1>" + tag + "<p>" + description + "</p></div>"

        var info = new google.maps.InfoWindow({
            content: content
        })
        info.addListener('closeclick', function() {
            info.fixed = false
        })

        marker.addListener('click', function() {
            info.fixed = true
            info.open(this.map, marker)
        })

        marker.addListener('mouseover', function() {
            info.open(this.map, marker)
        })

        marker.addListener('mouseout', function() {
            if (!info.fixed) {
                info.fixed = false
                info.close()
            }
        })

        markers.push(marker)

        return marker
    },

    //Remove all markers from the map
    removeMarkers: function() {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(null)
            markers[i] = null
        }
        markers = [];
    },

    //Place markers on the map for all events the user is interested in
    showInterestedEvents: function() {
        window.map.removeMarkers()
        // Call to events api endpoint (returns events specified user is interested in)
        sendEventsAjax('interests', null)
    },

    //Place markers on the map for events of a specific interest
    showSpecificEvents: function(tag) {
        window.map.removeMarkers()
        // Call to events api endpoint (returns events of the specific tag)
        sendEventsAjax('interests', tag)
    },

    //Place markers on the map for all the events
    showAllEvents: function() {
        window.map.removeMarkers()
        // Call to events api endpoint (returns all the events)
        sendEventsAjax('all', null)
    }
}