require('./bootstrap.js')
const flatpickr = require("flatpickr")

if($("#map").length)
    window.map = require('./map.js')

require('./utils.js')

if($(".event").length)
    require("./event.js")

require('./events.js')