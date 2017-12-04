// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.

if ($("#map-filters").length)
    require('./map-filters.js')
if ($("#event-form").length)
    require('./event-form.js')

let map
let markers = []

function sendEventsAjax(scope = undefined, tag = undefined, text = undefined, date = undefined) {
    let scopes = []

    if (scope)
        scopes.push(scope)
    if (tag)
        scopes.push('tag')
    if (text)
        scopes.push('name')
    if (date)
        scopes.push('date')

    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/events/api/",
        data: {
            scopes: scopes,
            tag: tag,
            text: text,
            date: date
        },
        success: (events) => {

            //Create markers on the map depending on the events returned
            for (i = 0; i < events.length; i++) {
                let data = events[i]
                window.map.createMarker(data.name,
                    data.description, data.id, data.tag_code, {
                        lat: data.latitude,
                        lng: data.longitude
                    })
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
            infoWindow.setPosition(pos)
            infoWindow.setContent(browserHasGeolocation ?
                'Error: The Geolocation service failed.' :
                'Error: Your browser doesn\'t support geolocation.')
            infoWindow.open(map)
        }

        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                let pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                }

                // let iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
                let iconBase = 'http://maps.gstatic.com/mapfiles/ms2/micons/'
                let marker = new google.maps.Marker({
                    position: new google.maps.LatLng(pos.lat, pos.lng),
                    map: map,
                    animation: google.maps.Animation.DROP,
                    icon: iconBase + 'blue.png'
                })

                map.setCenter(pos)

            }, function() {
                handleLocationError(true, new google.maps.InfoWindow, map.getCenter())
            }, {timeout:10000})

        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, new google.maps.InfoWindow, map.getCenter())
        }

        window.map.showEvents({ scope: 'all' })

        //Google's drawing manager (Marker and Hand tools)
        let drawingManager = new google.maps.drawing.DrawingManager({
            drawingControl: true,
            drawingControlOptions: {
                position: google.maps.ControlPosition.TOP_LEFT,
                //Only need a marker from the tools, hand is default
                drawingModes: ['marker'],
                draggable: true
            },
            //Marker should be draggable
            markerOptions: { draggable: true }
        })

        drawingManager.setMap(map)

        // Change the text that appears when hovering over the hand or marker
        $(map.getDiv()).one('mouseover', 'img[src="https://maps.gstatic.com/mapfiles/drawing.png"]', function(e) {
            $(e.delegateTarget).find('img[src="https://maps.gstatic.com/mapfiles/drawing.png"]').each(function() {
                $(this).closest('div[title]').attr('title', function() {
                    switch (this.title) {
                        case 'Add a marker':
                            return 'Add me to the map and create an event!'
                        case 'Stop drawing':
                            return ''
                        default:
                            return this.title
                    }
                })
            })
        })
        // Function called when marker is placed
        google.maps.event.addListener(drawingManager, 'markercomplete', function(marker) {
            drawingManager.set('drawingMode')

            showEventForm(marker.getPosition().lat(), marker.getPosition().lng())

            window.currentMarker = marker
        })
    },

    // Create marker given event data
    createMarker: function(name, description, id, tag, coords) {
        let iconBase = 'http://maps.gstatic.com/mapfiles/ms2/micons/'
        let marker = new google.maps.Marker({
            position: new google.maps.LatLng(coords.lat, coords.lng),
            map: map,
            animation: google.maps.Animation.DROP,
            icon: iconBase + 'red-pushpin.png'
        })

        let content = "<h1><div class='event-info'>" + name + "</h1>" + (tag ? tag : '') + "<p>" + description + "</p></div>"

        let info = new google.maps.InfoWindow({
            content: content
        })
        info.addListener('closeclick', function() {
            info.fixed = false
        })

        marker.addListener('click', function() {
            location.href = "/events/" + id
        })

        marker.addListener('mouseover', function() {
            info.open(this.map, marker)
        })

        marker.addListener('mouseout', function() {
            info.close()
        })

        markers.push(marker)

        return marker
    },

    //Remove all markers from the map
    removeMarkers: function() {
        for (let i = 0; i < markers.length; i++) {
            markers[i].setMap(null)
            markers[i] = null
        }
        markers = []
    },

    //Place markers on the map for all events the user is interested in
    showEvents: function(opts) {
        window.map.removeMarkers()
        // Call to events api endpoint (returns events specified user is interested in)
        sendEventsAjax(opts.scope, opts.tag, opts.name, opts.date)
    },
}