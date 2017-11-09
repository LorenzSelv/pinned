require('./bootstrap.js')
const flatpickr = require("flatpickr")

if($("#map").length)
    window.map = require('./map.js')

require('./utils.js')


require('./events.js')

require('./profile.js')

if($(".event").length)
    require("./event.js")

require('./events.js')
