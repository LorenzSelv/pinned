const bootstrap = require('./bootstrap.js')
const flatpickr = require("flatpickr")
require('./utils.js')

if ($("#map").length) {
    require('./map-filters.js')
    window.map = require('./map.js')
}

if ($(".event").length)
    require("./event.js")
if($(".event-card").length)
    require("./event-card.js")

if ($(".profile-title").length)
    require('./profile.js')

if ($("#event-form").length)
    require('./events.js')