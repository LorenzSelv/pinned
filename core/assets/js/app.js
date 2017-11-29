// Require commonly used js files
require('./bootstrap.js')
require('./utils.js')

// Require map related files
if ($("#map").length) {
    const flatpickr = require("flatpickr")
    require('./map-filters.js')
    window.map = require('./map.js')
}

// Require event page files
if ($(".event").length)
    require("./event.js")

// Require event-card files
if($(".event-card").length)
    require("./event-card.js")

// Require profile page files
if ($(".profile-title").length)
    require('./profile.js')